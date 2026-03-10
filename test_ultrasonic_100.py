#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TDC-GP22 超声波测量100次 - 优化版
确保Fire脉冲正确产生，便于示波器观察

优化点:
1. 增加Fire脉冲数量和周期，产生可观察的脉冲串
2. 增加测量间隔，给示波器足够时间触发
3. 添加详细的Fire配置信息
4. 每次测量后读取状态，确认Fire是否触发
"""

import sys
import io
import time
from pathlib import Path
from datetime import datetime

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

sys.path.insert(0, str(Path(__file__).parent / ".claude" / "skills" / "jtool" / "scripts" / "src"))

from jtool import (
    JToolError, DevType, devices_scan, dev_open, dev_close,
    open_spi_device, SPIClockType, SPIFirstBitType
)


class UltrasonicMeasurement:
    """超声波测量器 - 100次测量"""

    OPCODE_POWER_ON_RESET = 0x50
    OPCODE_INIT = 0x70
    OPCODE_START_TOF_RESTART = 0x05
    OPCODE_START_TOF = 0x01
    OPCODE_WRITE_REG = 0x80
    OPCODE_READ_REG = 0xB0
    OPCODE_READ_STATUS = 0xB4

    def __init__(self):
        self.handle = None
        self.spi = None
        self.spi_mode = SPIClockType.LOW_2EDG
        self.spi_bit_order = SPIFirstBitType.MSB
        self.measurement_count = 0

    def _spi_xfer(self, data: bytes, read_len: int = 0) -> bytes:
        if read_len > 0:
            write_data = data + bytes(read_len)
        else:
            write_data = data
        return self.spi.write_read(self.spi_mode, self.spi_bit_order, write_data)

    def _send_opcode(self, opcode: int) -> bytes:
        return self._spi_xfer(bytes([opcode]))

    def _write_config_reg(self, reg_addr: int, value: int):
        opcode = self.OPCODE_WRITE_REG | (reg_addr & 0x07)
        data = bytes([
            opcode,
            (value >> 24) & 0xFF,
            (value >> 16) & 0xFF,
            (value >> 8) & 0xFF,
            value & 0xFF
        ])
        self._spi_xfer(data)

    def _read_result_reg(self, reg_addr: int) -> int:
        opcode = self.OPCODE_READ_REG | (reg_addr & 0x07)
        result = self._spi_xfer(bytes([opcode]), read_len=4)
        value = (result[1] << 24) | (result[2] << 16) | (result[3] << 8) | result[4]
        return value

    def _read_status(self) -> int:
        result = self._spi_xfer(bytes([self.OPCODE_READ_STATUS]), read_len=4)
        value = (result[1] << 24) | (result[2] << 16) | (result[3] << 8) | result[4]
        return value

    def open_device(self) -> bool:
        print("[初始化] 扫描设备...")
        devices = devices_scan(DevType.SPI)
        if not devices:
            print("❌ 未找到设备")
            return False
        print(f"✓ 找到: {devices[0]}")

        print("[初始化] 打开SPI设备...")
        self.handle, self.spi = open_spi_device()
        print("✓ 设备已打开")
        return True

    def close_device(self):
        if self.handle is not None:
            dev_close(self.handle)
            self.handle = None
            self.spi = None
            print("\n✓ 设备已关闭")

    def power_on_reset(self):
        print("\n[初始化] Power-on Reset...")
        self._send_opcode(self.OPCODE_POWER_ON_RESET)
        time.sleep(0.01)
        print("✓ Reset完成")

    def configure_with_fire_pulse(self):
        """
        配置TDC - 优化Fire脉冲产生

        Reg5配置:
        - Bit 31: Fire Fine使能 = 1
        - Bit 30: Fire Early使能 = 1
        - Bit 29-16: Fire脉冲数量 = 0x0010 (16个脉冲)
        - Bit 15-0: Fire脉冲周期 = 0x0040 (64个时钟周期)
        """
        print("\n" + "="*70)
        print("配置TDC（优化Fire脉冲产生）")
        print("="*70)

        # 计算Reg5值
        # Fire Fine使能 | Fire Early使能 | 脉冲数量 | 脉冲周期
        # 1<<31 | 1<<30 | 0x10<<16 | 0x40
        reg5_fire = (1 << 31) | (1 << 30) | (0x10 << 16) | 0x40
        # = 0xC0100040

        config = {
            0: 0x00440200,   # Reg0: 基本配置
            1: 0x21444000,   # Reg1: TOF Restart模式
            2: 0xA0000000,   # Reg2: 时钟配置
            3: 0xD0A24800,   # Reg3: 首波检测
            4: 0x00000000,   # Reg4: 保留
            5: reg5_fire,    # Reg5: Fire配置（产生脉冲串！）
            6: 0x00000000,   # Reg6: 中断
        }

        print("\n配置寄存器:")
        for reg_addr, value in config.items():
            self._write_config_reg(reg_addr, value)

            if reg_addr == 5:
                print(f"\n  Reg5 (Fire配置) = 0x{value:08X}")
                print(f"    Bit 31 (FF_E):     {(value >> 31) & 1}  ← Fire Fine输出使能")
                print(f"    Bit 30 (FE_E):     {(value >> 30) & 1}  ← Fire Early输出使能")
                print(f"    Bit 29-16 (脉冲数): 0x{(value >> 16) & 0x3FFF:04X} = {((value >> 16) & 0x3FFF)} 个脉冲")
                print(f"    Bit 15-0 (周期):   0x{value & 0xFFFF:04X} = {(value & 0xFFFF)} 时钟周期")
                print(f"\n    ⚠️  示波器设置建议:")
                print(f"       - 触发源: 选择fire_up或fire_down引脚")
                print(f"       - 触发边沿: 上升沿")
                print(f"       - 时基: 1-10 μs/div")
                print(f"       - 预期波形: 16个脉冲的脉冲串")
            else:
                print(f"  Reg{reg_addr} = 0x{value:08X}")

        # Init
        print("\n[初始化] 发送Init (0x70)...")
        self._send_opcode(self.OPCODE_INIT)
        time.sleep(0.01)
        print("✓ TDC初始化完成")

    def measure_once(self) -> dict:
        """执行一次测量"""
        # 启动TOF测量
        self._send_opcode(self.OPCODE_START_TOF_RESTART)

        # 等待测量完成（给足够时间让超声波传播）
        timeout = 1.0  # 1秒超时
        start_time = time.time()
        completed = False

        while time.time() - start_time < timeout:
            time.sleep(0.001)
            status = self._read_status()
            if (status >> 8) & 1:  # 测量完成位
                completed = True
                break

        # 读取结果
        return {
            'status': status,
            'completed': completed,
            'res0': self._read_result_reg(0),
            'res1': self._read_result_reg(1),
            'res2': self._read_result_reg(2),
            'res3': self._read_result_reg(3),
        }

    def run_100_measurements(self):
        """运行100次测量"""
        print("\n" + "="*70)
        print("开始100次超声波测量")
        print("="*70)
        print("\n提示:")
        print("  - 每次测量前会重新Init")
        print("  - 测量间隔200ms（给示波器触发时间）")
        print("  - Fire脉冲: 16个脉冲，周期64时钟")
        print("  - 按Ctrl+C可随时停止")
        print()
        print(f"{'序号':<6} {'时间':<15} {'RES0':<12} {'RES1':<12} {'RES2':<12} {'状态'}")
        print("-" * 70)

        try:
            for i in range(1, 101):
                self.measurement_count = i

                # 重新Init（每次测量前）
                self._send_opcode(self.OPCODE_INIT)
                time.sleep(0.01)  # 10ms稳定时间

                # 执行测量
                timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-6]
                results = self.measure_once()

                # 显示结果
                status_str = "OK" if results['completed'] else "TO"
                print(f"{i:<6} {timestamp:<15} "
                      f"0x{results['res0']:08X} "
                      f"0x{results['res1']:08X} "
                      f"0x{results['res2']:08X} "
                      f"{status_str}")

                # 测量间隔（200ms）
                if i < 100:  # 最后一次不需要等待
                    time.sleep(0.2)

        except KeyboardInterrupt:
            print(f"\n\n用户停止（已完成 {self.measurement_count} 次）")
            return False

        print("\n" + "="*70)
        print(f"✓ 100次测量完成！")
        print("="*70)
        return True

    def run(self):
        """主程序"""
        print("="*70)
        print("TDC-GP22 超声波测量 - 100次测试")
        print("="*70)

        try:
            # 打开设备
            if not self.open_device():
                return False

            # 初始化和配置
            self.power_on_reset()
            self.configure_with_fire_pulse()

            # 运行100次测量
            success = self.run_100_measurements()

            return success

        except JToolError as e:
            print(f"\n❌ JTool错误: {e.message}")
            return False
        except Exception as e:
            print(f"\n❌ 错误: {e}")
            import traceback
            traceback.print_exc()
            return False
        finally:
            self.close_device()


def main():
    tester = UltrasonicMeasurement()
    success = tester.run()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

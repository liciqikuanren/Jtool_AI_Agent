#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TDC-GP22 超声波双向交替发波测量

功能:
- 第1次: fire_up 发射，测量
- 第2次: fire_down 发射，测量
- 第3次: fire_up 发射，测量
- 第4次: fire_down 发射，测量
- ...交替进行

通过配置 Reg5 的 Bit 31 和 Bit 30 来控制使用哪个通道:
- Reg5 = 0x80100040: 启用 fire_up (Fire Fine)
- Reg5 = 0x40100040: 启用 fire_down (Fire Early)

硬件连接:
- fire_up    -> 探头1 (或探头的发射端1)
- fire_down  -> 探头2 (或探头的发射端2)
- Start/Stop -> 探头的接收端
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


class UltrasonicAlternateMeasurement:
    """超声波双向交替测量器"""

    OPCODE_POWER_ON_RESET = 0x50
    OPCODE_INIT = 0x70
    OPCODE_START_TOF_RESTART = 0x05
    OPCODE_START_TOF = 0x01
    OPCODE_WRITE_REG = 0x80
    OPCODE_READ_REG = 0xB0
    OPCODE_READ_STATUS = 0xB4

    def __init__(self, cycles=100, interval_ms=200):
        self.cycles = cycles
        self.interval_ms = interval_ms
        self.handle = None
        self.spi = None
        self.spi_mode = SPIClockType.LOW_2EDG
        self.spi_bit_order = SPIFirstBitType.MSB
        self.current_cycle = 0

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

    def configure_for_fire_up(self):
        """配置使用 fire_up (Fire Fine) 发射"""
        # Reg5: fire_up 启用, fire_down 禁用
        # Bit 31 = 1 (FF_E), Bit 30 = 0 (FE_E)
        reg5_fire_up = (1 << 31) | (0x10 << 16) | 0x40
        # = 0x80100040

        self._write_config_reg(5, reg5_fire_up)
        return reg5_fire_up

    def configure_for_fire_down(self):
        """配置使用 fire_down (Fire Early) 发射"""
        # Reg5: fire_down 启用, fire_up 禁用
        # Bit 31 = 0 (FF_E), Bit 30 = 1 (FE_E)
        reg5_fire_down = (1 << 30) | (0x10 << 16) | 0x40
        # = 0x40100040

        self._write_config_reg(5, reg5_fire_down)
        return reg5_fire_down

    def configure_base(self):
        """配置基础寄存器"""
        print("\n" + "="*70)
        print("配置TDC基础参数")
        print("="*70)

        config = {
            0: 0x00440200,
            1: 0x21444000,  # TOF Restart模式
            2: 0xA0000000,
            3: 0xD0A24800,
            4: 0x00000000,
            # Reg5 在每次测量前动态配置
            6: 0x00000000,
        }

        for reg_addr, value in config.items():
            self._write_config_reg(reg_addr, value)
            print(f"  Reg{reg_addr} = 0x{value:08X}")

    def measure_once(self, fire_channel: str) -> dict:
        """
        执行一次测量
        Args:
            fire_channel: 'up' 或 'down'
        """
        # 根据通道配置Reg5
        if fire_channel == 'up':
            reg5 = self.configure_for_fire_up()
            channel_name = "fire_up"
        else:
            reg5 = self.configure_for_fire_down()
            channel_name = "fire_down"

        # Init（关键：每次切换通道后必须Init）
        self._send_opcode(self.OPCODE_INIT)
        time.sleep(0.005)

        # 启动测量
        self._send_opcode(self.OPCODE_START_TOF_RESTART)

        # 等待测量完成
        timeout = 0.5
        start_time = time.time()
        completed = False

        while time.time() - start_time < timeout:
            time.sleep(0.001)
            status = self._read_status()
            if (status >> 8) & 1:
                completed = True
                break

        # 读取结果
        return {
            'channel': channel_name,
            'reg5': reg5,
            'status': status,
            'completed': completed,
            'res0': self._read_result_reg(0),
            'res1': self._read_result_reg(1),
            'res2': self._read_result_reg(2),
            'res3': self._read_result_reg(3),
        }

    def run_alternate_measurement(self):
        """运行双向交替测量"""
        print("\n" + "="*70)
        print(f"开始双向交替测量 - 共 {self.cycles} 次")
        print("="*70)
        print("\n模式:")
        print("  奇数次: fire_up 发射 → 测量")
        print("  偶数次: fire_down 发射 → 测量")
        print("\n示波器建议:")
        print("  - CH1: fire_up 引脚")
        print("  - CH2: fire_down 引脚")
        print("  - 触发: 任一通道上升沿")
        print("  - 时基: 10-50 μs/div")
        print()
        print(f"{'序号':<6} {'通道':<12} {'时间':<15} {'RES0':<12} {'状态'}")
        print("-" * 70)

        try:
            for i in range(1, self.cycles + 1):
                self.current_cycle = i

                # 确定使用哪个通道
                if i % 2 == 1:  # 奇数
                    fire_channel = 'up'
                    channel_display = "fire_up ↑"
                else:  # 偶数
                    fire_channel = 'down'
                    channel_display = "fire_down ↓"

                # 执行测量
                timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-6]
                results = self.measure_once(fire_channel)

                # 显示结果
                status_str = "OK" if results['completed'] else "TO"
                print(f"{i:<6} {channel_display:<12} {timestamp:<15} "
                      f"0x{results['res0']:08X} {status_str}")

                # 测量间隔
                if i < self.cycles:
                    time.sleep(self.interval_ms / 1000.0)

        except KeyboardInterrupt:
            print(f"\n\n用户停止（已完成 {self.current_cycle} 次）")
            return False

        print("\n" + "="*70)
        print(f"✓ {self.cycles}次双向交替测量完成！")
        print("="*70)
        return True

    def run(self):
        """主程序"""
        print("="*70)
        print("TDC-GP22 超声波双向交替发波测量")
        print("="*70)
        print(f"测量次数: {self.cycles}")
        print(f"间隔时间: {self.interval_ms} ms")
        print()
        print("Fire通道配置:")
        print(f"  fire_up   (奇数次): Reg5 = 0x80100040")
        print(f"  fire_down (偶数次): Reg5 = 0x40100040")
        print("="*70)

        try:
            # 打开设备
            if not self.open_device():
                return False

            # 初始化和基础配置
            self.power_on_reset()
            self.configure_base()

            # 发送Init
            print("\n[初始化] 发送Init...")
            self._send_opcode(self.OPCODE_INIT)
            time.sleep(0.01)

            # 运行交替测量
            success = self.run_alternate_measurement()

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
    import argparse

    parser = argparse.ArgumentParser(description='TDC-GP22 双向交替测量')
    parser.add_argument('-n', '--cycles', type=int, default=100,
                        help='测量次数（默认100）')
    parser.add_argument('-i', '--interval', type=int, default=200,
                        help='测量间隔ms（默认200）')
    args = parser.parse_args()

    tester = UltrasonicAlternateMeasurement(
        cycles=args.cycles,
        interval_ms=args.interval
    )
    success = tester.run()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TDC-GP22 周期性测量程序
适用于接了超声波探头的场景（自发自收模式）

配置说明:
- Fire通道: 启用（驱动超声波探头）
- 测量模式: Start_TOF_Restart (往返飞行时间)
- 周期性: 可配置（默认100ms间隔）

硬件连接:
- fire_up/down -> 超声波探头
- Start/Stop -> 可接外部触发或内部循环
"""

import sys
import io
import time
from pathlib import Path
from datetime import datetime

# 设置UTF-8输出
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

sys.path.insert(0, str(Path(__file__).parent / ".claude" / "skills" / "jtool" / "scripts" / "src"))

from jtool import (
    JToolError, DevType, devices_scan, dev_open, dev_close,
    open_spi_device, SPIClockType, SPIFirstBitType
)


class TDCPeriodicMeasurement:
    """TDC-GP22 周期性测量器"""

    # 操作码
    OPCODE_POWER_ON_RESET = 0x50
    OPCODE_INIT = 0x70
    OPCODE_START_TOF_RESTART = 0x05  # 往返飞行时间测量（推荐用于探头）
    OPCODE_START_TOF = 0x01          # 单次飞行时间测量
    OPCODE_WRITE_REG = 0x80
    OPCODE_READ_REG = 0xB0
    OPCODE_READ_STATUS = 0xB4

    def __init__(self, interval_ms=100, max_cycles=None):
        """
        初始化
        Args:
            interval_ms: 测量间隔（毫秒）
            max_cycles: 最大测量次数（None=无限循环）
        """
        self.interval_ms = interval_ms
        self.max_cycles = max_cycles
        self.handle = None
        self.spi = None
        self.spi_mode = SPIClockType.LOW_2EDG  # CPOL=0, CPHA=1
        self.spi_bit_order = SPIFirstBitType.MSB
        self.cycle_count = 0

    def _spi_xfer(self, data: bytes, read_len: int = 0) -> bytes:
        """SPI数据传输"""
        if read_len > 0:
            write_data = data + bytes(read_len)
        else:
            write_data = data
        return self.spi.write_read(self.spi_mode, self.spi_bit_order, write_data)

    def _send_opcode(self, opcode: int) -> bytes:
        """发送单字节操作码"""
        return self._spi_xfer(bytes([opcode]))

    def _write_config_reg(self, reg_addr: int, value: int):
        """写入配置寄存器"""
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
        """读取结果寄存器（32位）"""
        opcode = self.OPCODE_READ_REG | (reg_addr & 0x07)
        result = self._spi_xfer(bytes([opcode]), read_len=4)
        value = (result[1] << 24) | (result[2] << 16) | (result[3] << 8) | result[4]
        return value

    def _read_status(self) -> int:
        """读取状态寄存器"""
        result = self._spi_xfer(bytes([self.OPCODE_READ_STATUS]), read_len=4)
        value = (result[1] << 24) | (result[2] << 16) | (result[3] << 8) | result[4]
        return value

    def open_device(self) -> bool:
        """打开JTool设备"""
        print("[初始化] 扫描JTool SPI设备...")
        devices = devices_scan(DevType.SPI)
        if not devices:
            print("❌ 未找到SPI设备")
            return False
        print(f"✓ 找到设备: {devices[0]}")

        print("[初始化] 打开SPI设备...")
        self.handle, self.spi = open_spi_device()
        print("✓ SPI设备已打开")
        print(f"  模式: CPOL=0, CPHA=1 (LOW_2EDG)")
        print(f"  位序: MSB")
        return True

    def close_device(self):
        """关闭设备"""
        if self.handle is not None:
            dev_close(self.handle)
            self.handle = None
            self.spi = None
            print("\n✓ 设备已关闭")

    def power_on_reset(self):
        """Power-on Reset"""
        print("[初始化] Power-on Reset...")
        self._send_opcode(self.OPCODE_POWER_ON_RESET)
        time.sleep(0.01)
        print("✓ Reset完成")

    def configure_tdc(self):
        """
        配置TDC（启用Fire通道，用于驱动超声波探头）
        """
        print("\n[初始化] 配置TDC参数...")
        print("-" * 60)

        # 配置寄存器（启用Fire，适合超声波探头）
        config = {
            0: 0x00440200,  # Reg0: 基本TDC配置
            1: 0x21444000,  # Reg1: 测量模式（TOF Restart模式）
            2: 0xA0000000,  # Reg2: 时钟配置
            3: 0xD0A24800,  # Reg3: 首波检测配置
            4: 0x00000000,  # Reg4: 保留
            5: 0xC0000000,  # Reg5: Fire配置（启用！）
            6: 0x00000000,  # Reg6: 中断配置
        }

        print("写入配置寄存器:")
        for reg_addr, value in config.items():
            self._write_config_reg(reg_addr, value)
            if reg_addr == 5:
                print(f"  Reg5 (Fire) = 0x{value:08X}")
                print(f"    Bit 31 (FF_E) = 1  ← Fire Fine 启用")
                print(f"    Bit 30 (FE_E) = 1  ← Fire Early 启用")
                print(f"    ✓ Fire通道已启用（驱动超声波探头）")
            else:
                print(f"  Reg{reg_addr} = 0x{value:08X}")

        # Init
        print("\n[初始化] 发送Init (0x70)...")
        self._send_opcode(self.OPCODE_INIT)
        time.sleep(0.01)
        print("✓ TDC初始化完成")

    def measure_once(self) -> dict:
        """
        执行一次测量
        Returns:
            测量结果字典
        """
        # 启动测量（TOF Restart模式 - 适合往返测量）
        self._send_opcode(self.OPCODE_START_TOF_RESTART)

        # 等待测量完成
        timeout = 0.5  # 500ms超时
        start_time = time.time()
        completed = False

        while time.time() - start_time < timeout:
            time.sleep(0.001)  # 1ms轮询
            status = self._read_status()

            # 检查测量完成位 (Bit 8)
            if (status >> 8) & 1:
                completed = True
                break

        # 读取结果
        results = {
            'status': status,
            'completed': completed,
            'res0': self._read_result_reg(0),
            'res1': self._read_result_reg(1),
            'res2': self._read_result_reg(2),
            'res3': self._read_result_reg(3),
        }

        return results

    def format_result(self, results: dict) -> str:
        """格式化测量结果"""
        status_str = "完成" if results['completed'] else "超时"

        # 计算时间值（如果RES_0有效）
        res0 = results['res0']
        if res0 != 0 and res0 != 0xFFFFFFFF:
            # TDC-GP22 典型分辨率约 90ps
            # 原始值转换为时间（简化计算）
            time_ns = res0 * 90.0 / 1000.0  # 转换为ns
            time_str = f"{time_ns:.2f} ns"
        else:
            time_str = "无效"

        return f"状态:{status_str} RES0:0x{res0:08X} ({time_str}) RES1:0x{results['res1']:08X}"

    def run(self):
        """运行周期性测量"""
        print("=" * 70)
        print("TDC-GP22 周期性测量程序")
        print("=" * 70)
        print(f"测量间隔: {self.interval_ms} ms")
        print(f"最大次数: {'无限' if self.max_cycles is None else self.max_cycles}")
        print(f"Fire通道: 启用（驱动超声波探头）")
        print(f"测量模式: TOF Restart（往返飞行时间）")
        print("=" * 70)
        print()

        try:
            # 打开设备
            if not self.open_device():
                return False

            # 初始化和配置
            self.power_on_reset()
            self.configure_tdc()

            print("\n" + "=" * 70)
            print("开始周期性测量（按Ctrl+C停止）")
            print("=" * 70)
            print()
            print(f"{'序号':<8} {'时间':<20} {'测量结果'}")
            print("-" * 70)

            # 测量循环
            while True:
                self.cycle_count += 1

                # 检查最大次数
                if self.max_cycles and self.cycle_count > self.max_cycles:
                    print(f"\n已达到最大测量次数 ({self.max_cycles})")
                    break

                # 执行测量
                timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                results = self.measure_once()

                # 显示结果
                result_str = self.format_result(results)
                print(f"{self.cycle_count:<8} {timestamp:<20} {result_str}")

                # 重新Init（准备下一次测量）
                self._send_opcode(self.OPCODE_INIT)
                time.sleep(0.005)  # 5ms延时

                # 等待到下一个周期
                time.sleep(self.interval_ms / 1000.0)

        except KeyboardInterrupt:
            print(f"\n\n用户停止（已测量 {self.cycle_count} 次）")
        except JToolError as e:
            print(f"\n❌ JTool错误: {e.message} (代码: {e.code})")
            return False
        except Exception as e:
            print(f"\n❌ 错误: {e}")
            import traceback
            traceback.print_exc()
            return False
        finally:
            self.close_device()
            print(f"\n总计测量次数: {self.cycle_count}")

        return True


def main():
    import argparse

    parser = argparse.ArgumentParser(description='TDC-GP22 周期性测量')
    parser.add_argument('-i', '--interval', type=int, default=100,
                        help='测量间隔（毫秒，默认100）')
    parser.add_argument('-n', '--count', type=int, default=None,
                        help='最大测量次数（默认无限）')
    args = parser.parse_args()

    # 创建测量器
    tester = TDCPeriodicMeasurement(
        interval_ms=args.interval,
        max_cycles=args.count
    )

    # 运行
    success = tester.run()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

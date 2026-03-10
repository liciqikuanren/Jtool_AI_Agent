#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TDC-GP22 修改配置后读取 B5 (RES_5) 等寄存器

流程:
1. Power-on Reset
2. 写入新的配置到 Reg0-Reg6
3. 发送 Init (0x70)
4. 启动校准测量
5. 读取 5 个结果寄存器 (B0-B4)
6. 再次修改配置
7. 再次读取，查看数值变化
"""

import sys
import io
import time
from pathlib import Path

# 设置UTF-8输出
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

sys.path.insert(0, str(Path(__file__).parent / ".claude" / "skills" / "jtool" / "scripts" / "src"))

from jtool import (
    JToolError, DevType, devices_scan, dev_open, dev_close,
    open_spi_device, SPIClockType, SPIFirstBitType
)


class TDCGP22B5Tester:
    """TDC-GP22 B5 读取测试器"""

    # 操作码定义
    OPCODE_POWER_ON_RESET = 0x50
    OPCODE_INIT = 0x70
    OPCODE_START_CAL_RESONATOR = 0x03  # 校准 4MHz 谐振器
    OPCODE_START_CAL_TDC = 0x04        # 校准 TDC
    OPCODE_WRITE_REG = 0x80            # 写配置寄存器基地址
    OPCODE_READ_REG = 0xB0             # 读结果寄存器基地址

    def __init__(self):
        self.handle = None
        self.spi = None
        self.spi_mode = SPIClockType.LOW_2EDG  # CPOL=0, CPHA=1
        self.spi_bit_order = SPIFirstBitType.MSB

    def _spi_xfer(self, data: bytes, read_len: int = 0) -> bytes:
        """SPI 数据传输"""
        if read_len > 0:
            write_data = data + bytes(read_len)
        else:
            write_data = data
        result = self.spi.write_read(self.spi_mode, self.spi_bit_order, write_data)
        return result

    def _send_opcode(self, opcode: int) -> bytes:
        """发送单字节操作码"""
        return self._spi_xfer(bytes([opcode]))

    def _write_config_reg(self, reg_addr: int, value: int) -> bytes:
        """写入配置寄存器 (32位)"""
        opcode = self.OPCODE_WRITE_REG | (reg_addr & 0x07)
        data = bytes([
            opcode,
            (value >> 24) & 0xFF,
            (value >> 16) & 0xFF,
            (value >> 8) & 0xFF,
            value & 0xFF
        ])
        return self._spi_xfer(data)

    def _read_result_reg(self, reg_addr: int) -> int:
        """读取结果寄存器 (32位)"""
        opcode = self.OPCODE_READ_REG | (reg_addr & 0x07)
        result = self._spi_xfer(bytes([opcode]), read_len=4)
        value = (result[1] << 24) | (result[2] << 16) | (result[3] << 8) | result[4]
        return value

    def open(self) -> bool:
        """打开 JTool SPI 设备"""
        print("[1] 扫描 JTool SPI 设备...")
        devices = devices_scan(DevType.SPI)
        if not devices:
            print("❌ 未找到 SPI 设备")
            return False
        print(f"✓ 找到设备: {devices[0]}")

        print("\n[2] 打开 SPI 设备...")
        self.handle, self.spi = open_spi_device()
        print("✓ SPI 设备已打开")
        print(f"  模式: CPOL=0, CPHA=1")
        return True

    def close(self):
        """关闭设备"""
        if self.handle is not None:
            dev_close(self.handle)
            self.handle = None
            self.spi = None
            print("\n✓ 设备已关闭")

    def power_on_reset(self):
        """Power-on Reset"""
        print("\n[3] Power-on Reset (0x50)...")
        self._send_opcode(self.OPCODE_POWER_ON_RESET)
        time.sleep(0.01)
        print("✓ Reset 完成")

    def read_5_params(self, label=""):
        """读取 5 个参数 (RES_0 到 RES_4)"""
        if label:
            print(f"\n{'-'*60}")
            print(f"读取 5 个参数 - {label}")
            print(f"{'-'*60}")
        else:
            print(f"\n{'-'*60}")
            print("读取 5 个参数")
            print(f"{'-'*60}")

        results = {}
        for i in range(5):
            value = self._read_result_reg(i)
            results[f"RES_{i}"] = value
            print(f"  操作码 B{i:X} -> RES_{i}: 0x{value:08X} ({value})")
        return results

    def write_config_and_measure(self, config_name, reg_values):
        """写入配置并启动测量"""
        print(f"\n{'='*60}")
        print(f"配置: {config_name}")
        print(f"{'='*60}")

        # 写入配置寄存器
        print("\n写入配置寄存器:")
        for reg_addr, value in reg_values.items():
            print(f"  Reg{reg_addr} = 0x{value:08X}")
            self._write_config_reg(reg_addr, value)

        # Init
        print("\n发送 Init (0x70)...")
        self._send_opcode(self.OPCODE_INIT)
        time.sleep(0.01)

        # 启动时钟校准测量 (产生新数据)
        print("\n启动 4MHz 时钟校准测量 (0x03)...")
        self._send_opcode(self.OPCODE_START_CAL_RESONATOR)
        time.sleep(0.2)  # 等待测量完成

        print("✓ 测量完成")

    def run_test(self):
        """完整测试流程"""
        print("=" * 60)
        print("TDC-GP22 修改配置后读取 B5 测试")
        print("=" * 60)

        try:
            # 打开设备
            if not self.open():
                return False

            # Power-on Reset
            self.power_on_reset()

            # 第一次读取 (复位后的默认值)
            print("\n" + "="*60)
            print("【第一次读取】- 复位后状态")
            print("="*60)
            results1 = self.read_5_params("复位后状态")

            # 写入配置 A 并测量
            config_a = {
                0: 0x00440200,  # 基本配置
                1: 0x21444000,  # 测量模式
                2: 0xA0000000,  # 时钟配置
                3: 0xD0A24800,  # 首波检测
                4: 0x00000000,
                5: 0x40000000,
                6: 0x00000000,
            }
            self.write_config_and_measure("配置 A (标准配置)", config_a)

            # 第二次读取
            print("\n" + "="*60)
            print("【第二次读取】- 使用配置 A 测量后")
            print("="*60)
            results2 = self.read_5_params("配置 A 测量后")

            # 写入配置 B (改变一些参数)
            config_b = {
                0: 0x00440200,  # 保持基本配置
                1: 0x31444000,  # 改变测量模式!
                2: 0xB0000000,  # 改变时钟配置!
                3: 0xE0A24800,  # 改变首波检测
                4: 0x00000000,
                5: 0x50000000,  # 改变 Fire 配置
                6: 0x00000000,
            }
            self.write_config_and_measure("配置 B (修改参数)", config_b)

            # 第三次读取
            print("\n" + "="*60)
            print("【第三次读取】- 使用配置 B 测量后")
            print("="*60)
            results3 = self.read_5_params("配置 B 测量后")

            # 对比结果
            print("\n" + "="*60)
            print("数值变化对比")
            print("="*60)
            print(f"{'寄存器':<10} {'复位后':<18} {'配置A后':<18} {'配置B后':<18}")
            print("-" * 64)
            for i in range(5):
                r1 = f"0x{results1[f'RES_{i}']:08X}"
                r2 = f"0x{results2[f'RES_{i}']:08X}"
                r3 = f"0x{results3[f'RES_{i}']:08X}"
                print(f"RES_{i:<6} {r1:<18} {r2:<18} {r3:<18}")

            # 检查是否有变化
            print("\n变化分析:")
            changed = False
            for i in range(5):
                if results1[f'RES_{i}'] != results2[f'RES_{i}'] or results2[f'RES_{i}'] != results3[f'RES_{i}']:
                    print(f"  ✓ RES_{i}: 数值已变化")
                    changed = True
            if not changed:
                print("  ⚠ 所有寄存器数值相同 (可能需要实际测量触发)")

            print("\n" + "="*60)
            print("测试完成!")
            print("="*60)

            return True

        except JToolError as e:
            print(f"\n❌ JTool 错误: {e.message} (代码: {e.code})")
            return False
        except Exception as e:
            print(f"\n❌ 错误: {e}")
            import traceback
            traceback.print_exc()
            return False
        finally:
            self.close()


def main():
    tester = TDCGP22B5Tester()
    success = tester.run_test()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

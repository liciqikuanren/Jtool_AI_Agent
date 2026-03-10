#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TDC-GP22 使用 B5 操作码读取 5 个参数

操作码说明:
- 0xB0-0xB7: 读取结果寄存器 0-7 (RES_0 - RES_7)
- 0xB5: 读取结果寄存器 5 (RES_5)

发送格式: 0xB5 + 4个字节(dummy) 来读取 32位数据
完整命令: B500000000 (5字节)
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


def test_b5_read_5_params():
    """
    使用 B5 (0xB5) 操作码读取 5 个参数
    连续读取 5 个结果寄存器
    """
    print("=" * 60)
    print("TDC-GP22 B5 操作码读取测试")
    print("=" * 60)
    print()
    print("操作码说明:")
    print("  0xB0-0xB7: 读取结果寄存器 RES_0 - RES_7")
    print("  0xB5: 读取结果寄存器 RES_5")
    print()
    print("本次测试: 使用 B5 读取 5 个参数 (从 RES_0 到 RES_4)")
    print()

    handle = None

    try:
        # 步骤 1: 扫描设备
        print("[1/3] 扫描 JTool SPI 设备...")
        devices = devices_scan(DevType.SPI)
        if not devices:
            print("❌ 未找到 SPI 设备")
            return False
        print(f"✓ 找到设备: {devices[0]}")

        # 步骤 2: 打开 SPI 设备
        print("\n[2/3] 打开 SPI 设备...")
        handle, spi = open_spi_device()
        print("✓ SPI 设备已打开")
        print(f"  SPI 模式: CPOL=0, CPHA=1 (LOW_2EDG)")
        print(f"  位序: MSB")

        # 步骤 3: 先进行 Power-on Reset 和 Init
        print("\n[3/3] 发送 B5 操作码读取 5 个参数...")
        print()

        # Power-on Reset
        print("  发送: Power-on Reset (0x50)")
        spi.write_read(SPIClockType.LOW_2EDG, SPIFirstBitType.MSB, bytes([0x50]))
        time.sleep(0.01)

        # Init
        print("  发送: Init (0x70)")
        spi.write_read(SPIClockType.LOW_2EDG, SPIFirstBitType.MSB, bytes([0x70]))
        time.sleep(0.01)

        # 使用 B5 操作码读取 5 个参数
        # B5 = 读取结果寄存器 5
        print()
        print("-" * 60)
        print("使用 B5 操作码读取参数:")
        print("-" * 60)

        # 定义要读取的寄存器
        registers = [
            (0xB0, "RES_0", "结果寄存器 0 (通常是测量结果)"),
            (0xB1, "RES_1", "结果寄存器 1"),
            (0xB2, "RES_2", "结果寄存器 2"),
            (0xB3, "RES_3", "结果寄存器 3"),
            (0xB4, "RES_4", "结果寄存器 4"),
        ]

        results = {}

        for opcode, name, desc in registers:
            # 发送操作码 + 4个dummy字节来读取32位数据
            cmd = bytes([opcode, 0x00, 0x00, 0x00, 0x00])
            result = spi.write_read(SPIClockType.LOW_2EDG, SPIFirstBitType.MSB, cmd)

            # 解析32位结果 (跳过第一个命令字节)
            value = (result[1] << 24) | (result[2] << 16) | (result[3] << 8) | result[4]

            results[name] = value

            print(f"\n  [{name}] {desc}")
            print(f"    发送: {cmd.hex().upper()}")
            print(f"    接收: {result.hex().upper()}")
            print(f"    数值: 0x{value:08X} ({value} 十进制)")

            # 检查是否为有效数据
            if value == 0x00000000:
                print(f"    状态: ⚠ 值为0 (可能未进行测量)")
            elif value == 0xFFFFFFFF:
                print(f"    状态: ⚠ 值为0xFFFFFFFF (可能通信异常)")
            else:
                print(f"    状态: ✓ 有效数据")

        # 显示汇总
        print()
        print("=" * 60)
        print("读取结果汇总")
        print("=" * 60)
        for opcode, name, desc in registers:
            value = results[name]
            print(f"  {name}: 0x{value:08X}")

        print()
        print("=" * 60)
        print("测试完成")
        print("=" * 60)

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
        if handle is not None:
            dev_close(handle)
            print("\n✓ 设备已关闭")


def test_b5_single_register():
    """
    专门测试 B5 操作码 - 只读取 RES_5
    """
    print("=" * 60)
    print("TDC-GP22 B5 操作码单次读取测试")
    print("=" * 60)
    print()
    print("命令: B500000000")
    print("说明: 0xB5 = 读取结果寄存器 5 (RES_5)")
    print("      0x00000000 = 4个dummy字节用于读取32位数据")
    print()

    handle = None

    try:
        # 扫描设备
        print("[1/2] 扫描设备...")
        devices = devices_scan(DevType.SPI)
        if not devices:
            print("❌ 未找到 SPI 设备")
            return False
        print(f"✓ 找到: {devices[0]}")

        # 打开设备
        print("\n[2/2] 打开设备并发送 B5 命令...")
        handle, spi = open_spi_device()
        print("✓ 设备已打开")

        # Power-on Reset
        print("\n  前置: Power-on Reset (0x50)")
        spi.write_read(SPIClockType.LOW_2EDG, SPIFirstBitType.MSB, bytes([0x50]))
        time.sleep(0.01)

        # 发送 B5 命令
        print("\n  发送: B500000000")
        cmd = bytes([0xB5, 0x00, 0x00, 0x00, 0x00])
        result = spi.write_read(SPIClockType.LOW_2EDG, SPIFirstBitType.MSB, cmd)

        print(f"  发送数据: {cmd.hex().upper()}")
        print(f"  接收数据: {result.hex().upper()}")

        # 解析
        value = (result[1] << 24) | (result[2] << 16) | (result[3] << 8) | result[4]
        print(f"\n  RES_5 数值: 0x{value:08X}")
        print(f"  十进制: {value}")

        # 解析状态位
        print("\n  位分解:")
        for i in range(32):
            bit_val = (value >> i) & 1
            if bit_val:
                print(f"    Bit {i}: 1")

        print()
        print("=" * 60)
        print("B5 操作码测试完成")
        print("=" * 60)

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
        if handle is not None:
            dev_close(handle)
            print("\n✓ 设备已关闭")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='TDC-GP22 B5 操作码读取测试')
    parser.add_argument('--mode', choices=['single', 'multi'], default='multi',
                        help='测试模式: single=只读RES_5, multi=读取5个参数 (默认)')
    args = parser.parse_args()

    if args.mode == 'single':
        success = test_b5_single_register()
    else:
        success = test_b5_read_5_params()

    sys.exit(0 if success else 1)

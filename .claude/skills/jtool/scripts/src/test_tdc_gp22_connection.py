#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TDC-GP22 标准连接测试
严格按照手册流程: Power-on Reset → 读取 ID 寄存器

手册参考: TDC-GP22 Datasheet DB_GP22_en V0.9
  - 章节 3.4: SPI Interface
  - 章节 3.2: Read Registers
  - Table 3-4: Opcodes

连接测试流程:
  1. Power-on Reset (Opcode 0x50)
  2. 读取 ID 寄存器 (Opcode 0xB7) - 返回 7 字节 ID
"""

import sys
import io
import time
from pathlib import Path

# 设置UTF-8输出
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

sys.path.insert(0, str(Path(__file__).parent))

from jtool import (
    JToolError, DevType, devices_scan, dev_open, dev_close,
    open_spi_device, SPIClockType, SPIFirstBitType
)

# TDC-GP22 Opcode 定义
OPCODE_POWER_ON_RESET = 0x50   # 上电复位
OPCODE_READ_ID = 0xB7          # 读取 ID 寄存器 (7字节)
OPCODE_INIT = 0x70             # 初始化

# SPI 模式: TDC-GP22 要求 CPOL=0, CPHA=1
SPI_MODE = SPIClockType.LOW_2EDG
SPI_BIT_ORDER = SPIFirstBitType.MSB


def test_tdc_gp22_connection():
    """
    TDC-GP22 标准连接测试
    按照手册流程读取 ID 寄存器验证通信
    """
    print("=" * 60)
    print("TDC-GP22 标准连接测试")
    print("=" * 60)
    print()
    print("测试流程 (按手册 Section 3.4):")
    print("  1. Power-on Reset (0x50)")
    print("  2. 读取 ID 寄存器 (0xB7)")
    print()

    handle = None

    try:
        # 步骤 1: 扫描设备
        print("[1/4] 扫描 JTool SPI 设备...")
        devices = devices_scan(DevType.SPI)
        if not devices:
            print("❌ 未找到 SPI 设备")
            return False
        print(f"✓ 找到设备: {devices[0]}")

        # 步骤 2: 打开 SPI 设备
        print("\n[2/4] 打开 SPI 设备...")
        handle, spi = open_spi_device()
        print("✓ SPI 设备已打开")
        print(f"  模式: CPOL=0, CPHA=1 (手册要求)")

        # 步骤 3: Power-on Reset
        print("\n[3/4] Power-on Reset (0x50)...")
        print("  发送: 0x50")

        # SSN 变低后发送 Reset 命令
        result = spi.write_read(SPI_MODE, SPI_BIT_ORDER, bytes([OPCODE_POWER_ON_RESET]))
        time.sleep(0.01)  # 10ms 延时等待芯片复位
        print("✓ Power-on Reset 完成")

        # 步骤 4: 读取 ID 寄存器 (关键测试!)
        print("\n[4/4] 读取 ID 寄存器 (0xB7)...")
        print("  发送: 0xB7 (Read ID)")
        print("  期望: 返回 7 字节 ID 数据")

        # 发送 Read ID 命令 + 7 个字节的 dummy 数据来读取响应
        # 手册说明: opcode 0xB7 后跟随 7 个字节，顺序是 ID0, ID1 ... ID6
        cmd = bytes([OPCODE_READ_ID]) + bytes(7)  # 0xB7 + 7个空字节
        result = spi.write_read(SPI_MODE, SPI_BIT_ORDER, cmd)

        print(f"  发送: {cmd.hex()}")
        print(f"  接收: {result.hex()}")

        # 解析 ID 数据 (跳过第一个命令字节)
        id_bytes = result[1:8]  # 取后面7个字节
        print(f"  ID 数据: {' '.join([f'{b:02X}' for b in id_bytes])}")

        # 判断结果
        if id_bytes == bytes([0x00] * 7) or id_bytes == bytes([0xFF] * 7):
            print()
            print("⚠ 芯片未响应 - 可能原因:")
            print("  1. TDC-GP22 未正确连接")
            print("  2. RSTN 引脚未接高电平 (必须接 3.3V)")
            print("  3. 电源问题 (VCC/VIO 需要 3.3V)")
            print("  4. 缺少 4MHz 时钟源")
            success = False
        else:
            print()
            print("✓ 芯片响应正常!")
            print(f"  ID: {id_bytes.hex().upper()}")

            # 尝试解析 ID (如果有已知模式)
            # TDC-GP22 ID 通常包含芯片型号信息
            if id_bytes[0] == 0x00:
                print("  状态: 可能是新芯片或已复位状态")
            else:
                print(f"  状态: ID 有效")

            success = True

        # 可选: 尝试 Init 后再读一次
        if success:
            print("\n  [可选] 发送 Init (0x70) 后再读取...")
            spi.write_read(SPI_MODE, SPI_BIT_ORDER, bytes([OPCODE_INIT]))
            time.sleep(0.01)

            result2 = spi.write_read(SPI_MODE, SPI_BIT_ORDER, cmd)
            id_bytes2 = result2[1:8]
            print(f"  Init 后 ID: {' '.join([f'{b:02X}' for b in id_bytes2])}")

        print()
        print("=" * 60)
        if success:
            print("测试结果: ✅ 通过 - TDC-GP22 连接正常")
        else:
            print("测试结果: ❌ 失败 - TDC-GP22 未响应")
        print("=" * 60)

        return success

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


def test_with_full_reset():
    """
    使用 GPIO 控制 RSTN 的完整复位测试
    (如果 RSTN 连接到 JTool GPIO)
    """
    print("=" * 60)
    print("TDC-GP22 硬件复位测试 (GPIO 控制 RSTN)")
    print("=" * 60)
    print()
    print("注意: 此测试需要 RSTN 引脚连接到 JTool GPIO")
    print()

    # 这里可以添加 GPIO 控制代码
    # 如果用户有连接 RSTN 到 GPIO，可以实现硬件复位

    print("请确保:")
    print("  1. TDC-GP22 的 RSTN 引脚连接到 JTool GPIO")
    print("  2. 或者手动将 RSTN 拉低至少 50ns 再拉高")
    print()
    print("标准连接测试建议使用软件复位 (0x50)")

    return False


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='TDC-GP22 连接测试')
    parser.add_argument('--gpio-reset', action='store_true',
                        help='使用 GPIO 控制 RSTN 复位 (需要硬件连接)')
    args = parser.parse_args()

    if args.gpio_reset:
        success = test_with_full_reset()
    else:
        success = test_tdc_gp22_connection()

    sys.exit(0 if success else 1)

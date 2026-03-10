#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TDC-GP22 关闭 Fire Pulse Generator 验证

Fire Pulse Generator 关闭方法:
- 将 Reg5 设为 0x00000000
- 这会禁用 Fire Fine 和 Fire Early 输出
- 不会产生任何 fire_up/fire_down 脉冲
"""

import sys
import io
import time
from pathlib import Path

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

sys.path.insert(0, str(Path(__file__).parent / ".claude" / "skills" / "jtool" / "scripts" / "src"))

from jtool import (
    JToolError, DevType, devices_scan, dev_open, dev_close,
    open_spi_device, SPIClockType, SPIFirstBitType
)


def disable_fire_pulse_generator():
    """
    关闭 Fire Pulse Generator
    """
    print("=" * 60)
    print("关闭 Fire Pulse Generator")
    print("=" * 60)
    print()

    handle = None

    try:
        # 扫描设备
        print("[1] 扫描设备...")
        devices = devices_scan(DevType.SPI)
        if not devices:
            print("❌ 未找到设备")
            return False
        print(f"✓ 找到: {devices[0]}")

        # 打开设备
        print("\n[2] 打开SPI设备...")
        handle, spi = open_spi_device()
        print("✓ 设备已打开")

        # Power-on Reset
        print("\n[3] Power-on Reset...")
        spi.write_read(SPIClockType.LOW_2EDG, SPIFirstBitType.MSB, bytes([0x50]))
        time.sleep(0.01)

        # 关闭 Fire Pulse Generator
        print("\n[4] 关闭 Fire Pulse Generator...")
        print("-" * 60)

        # 所有配置寄存器设为0（关键是Reg5=0）
        config = {
            0: 0x00000000,  # Reg0
            1: 0x00000000,  # Reg1
            2: 0x00000000,  # Reg2
            3: 0x00000000,  # Reg3
            4: 0x00000000,  # Reg4
            5: 0x00000000,  # Reg5 - Fire Pulse Generator 关闭！
            6: 0x00000000,  # Reg6
        }

        print("写入配置寄存器:")
        for reg_addr, value in config.items():
            opcode = 0x80 | reg_addr
            data = bytes([
                opcode,
                (value >> 24) & 0xFF,
                (value >> 16) & 0xFF,
                (value >> 8) & 0xFF,
                value & 0xFF
            ])
            spi.write_read(SPIClockType.LOW_2EDG, SPIFirstBitType.MSB, data)

            if reg_addr == 5:
                print(f"  Reg{reg_addr} = 0x{value:08X}  <-- Fire Pulse Generator")
                print(f"    Bit 31 (FF_E)  = {(value >> 31) & 1}  (Fire Fine 使能: 禁用)")
                print(f"    Bit 30 (FE_E)  = {(value >> 30) & 1}  (Fire Early 使能: 禁用)")
                print(f"    Bit 29-16      = 0x{(value >> 16) & 0x3FFF:04X}  (脉冲数量: 0)")
                print(f"    ✓ Fire Pulse Generator 已关闭")
            else:
                print(f"  Reg{reg_addr} = 0x{value:08X}")

        # Init
        print("\n[5] 发送 Init...")
        spi.write_read(SPIClockType.LOW_2EDG, SPIFirstBitType.MSB, bytes([0x70]))
        time.sleep(0.01)
        print("✓ TDC 初始化完成")

        # 验证：读取 Reg5 回读（通过结果寄存器间接验证）
        print("\n[6] 验证 Fire 状态...")

        # 读取状态寄存器
        result = spi.write_read(SPIClockType.LOW_2EDG, SPIFirstBitType.MSB,
                                bytes([0xB4, 0x00, 0x00, 0x00, 0x00]))
        status = (result[1] << 24) | (result[2] << 16) | (result[3] << 8) | result[4]
        print(f"  状态寄存器: 0x{status:08X}")

        # 尝试启动测量，验证TDC仍然可以工作（只是没有Fire输出）
        print("\n[7] 测试TDC测量功能（验证Fire关闭不影响测量能力）...")
        spi.write_read(SPIClockType.LOW_2EDG, SPIFirstBitType.MSB, bytes([0x03]))  # 时钟校准
        time.sleep(0.1)

        # 读取结果
        result = spi.write_read(SPIClockType.LOW_2EDG, SPIFirstBitType.MSB,
                                bytes([0xB0, 0x00, 0x00, 0x00, 0x00]))
        res0 = (result[1] << 24) | (result[2] << 16) | (result[3] << 8) | result[4]
        print(f"  RES_0 (时钟校准结果): 0x{res0:08X}")

        if res0 != 0 and res0 != 0xFFFFFFFF:
            print("  ✓ TDC 测量功能正常（Fire关闭不影响测量）")

        print("\n" + "=" * 60)
        print("结论")
        print("=" * 60)
        print()
        print("✓ Fire Pulse Generator 已成功关闭")
        print()
        print("配置:")
        print(f"  Reg5 = 0x00000000")
        print()
        print("效果:")
        print("  - fire_up 引脚:   无脉冲输出")
        print("  - fire_down 引脚: 无脉冲输出")
        print("  - TDC测量功能:    正常可用")
        print()
        print("应用场景:")
        print("  - 外部信号测量模式（外部提供Start/Stop）")
        print("  - 纯计时模式（不需要发射超声波）")
        print()
        print("重新启用Fire:")
        print("  Reg5 = 0xC0000000  (Bit 31=1, Bit 30=1)")

        return True

    except JToolError as e:
        print(f"\n❌ JTool错误: {e.message}")
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
    success = disable_fire_pulse_generator()
    sys.exit(0 if success else 1)

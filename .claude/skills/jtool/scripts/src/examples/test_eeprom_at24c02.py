#!/usr/bin/env python3
"""
AT24C02 EEPROM 测试示例

AT24C02是一款2Kbit（256字节）的I2C接口EEPROM。
- 页大小: 8字节
- I2C地址: 0x50-0x57 (由A2,A1,A0引脚决定)
- 写入后需要等待5ms才能进行下一次写入
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from jtool import (
    open_i2c_device, RegAddrType, JToolError,
    dev_close
)
import time


def test_at24c02(i2c_address: int = 0x50):
    """测试AT24C02 EEPROM"""

    print("=" * 60)
    print("AT24C02 EEPROM 测试")
    print("=" * 60)

    # 打开设备
    print("\n[1] 打开I2C设备...")
    handle, i2c = open_i2c_device()
    print(f"    ✓ 设备已打开")

    try:
        # 1. 扫描设备
        print(f"\n[2] 扫描I2C总线...")
        count, addresses = i2c.scan()
        print(f"    发现 {count} 个设备: {[f'0x{a:02X}' for a in addresses]}")

        if i2c_address not in addresses:
            print(f"    ✗ 未找到目标设备 (0x{i2c_address:02X})")
            return False
        print(f"    ✓ 目标设备 0x{i2c_address:02X} 在线")

        # 2. 单字节读写测试
        print(f"\n[3] 单字节读写测试...")
        test_data = bytes([0xA5, 0x5A, 0x12, 0x34, 0x56, 0x78, 0x90, 0xAB])

        for i, byte in enumerate(test_data):
            # 写入
            i2c.write(i2c_address, RegAddrType.BIT8, i, bytes([byte]))
            time.sleep(0.005)  # 等待写入完成

            # 读取验证
            read_data = i2c.read(i2c_address, RegAddrType.BIT8, i, 1)
            if read_data[0] != byte:
                print(f"    ✗ 地址 0x{i:02X}: 写入 0x{byte:02X}, 读取 0x{read_data[0]:02X}")
                return False

        print(f"    ✓ 单字节读写测试通过")

        # 3. 页写入测试 (页大小8字节)
        print(f"\n[4] 页写入测试 (页大小8字节)...")
        page_data = bytes(range(8))  # 0x00, 0x01, ... 0x07

        i2c.eeprom_write(i2c_address, RegAddrType.BIT8, 8, 0x10, page_data)
        time.sleep(0.005)

        # 读取验证
        read_data = i2c.read(i2c_address, RegAddrType.BIT8, 0x10, 8)
        if read_data != page_data:
            print(f"    ✗ 页写入失败")
            print(f"      期望: {page_data.hex()}")
            print(f"      实际: {read_data.hex()}")
            return False

        print(f"    ✓ 页写入测试通过")

        # 4. 跨页写入测试
        print(f"\n[5] 跨页写入测试...")
        cross_page_data = bytes(range(16))  # 跨越两页

        i2c.eeprom_write(i2c_address, RegAddrType.BIT8, 8, 0x18, cross_page_data)
        time.sleep(0.01)

        read_data = i2c.read(i2c_address, RegAddrType.BIT8, 0x18, 16)
        if read_data != cross_page_data:
            print(f"    ✗ 跨页写入失败")
            print(f"      期望: {cross_page_data.hex()}")
            print(f"      实际: {read_data.hex()}")
            return False

        print(f"    ✓ 跨页写入测试通过")

        # 5. 整片擦除/写入测试
        print(f"\n[6] 整片读写测试...")
        all_data = bytes([i & 0xFF for i in range(256)])

        print(f"    正在写入256字节数据...")
        i2c.eeprom_write(i2c_address, RegAddrType.BIT8, 8, 0x00, all_data)
        time.sleep(0.02)

        print(f"    正在读取验证...")
        read_data = i2c.read(i2c_address, RegAddrType.BIT8, 0x00, 256)

        if read_data != all_data:
            errors = sum(1 for i in range(256) if read_data[i] != all_data[i])
            print(f"    ✗ 整片读写失败，{errors} 字节错误")
            return False

        print(f"    ✓ 整片读写测试通过")

        print(f"\n" + "=" * 60)
        print("所有测试通过!")
        print("=" * 60)
        return True

    except JToolError as e:
        print(f"\n✗ JTool错误: {e.message}")
        return False
    except Exception as e:
        print(f"\n✗ 错误: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        dev_close(handle)
        print("\n设备已关闭")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='AT24C02 EEPROM测试')
    parser.add_argument('--addr', '-a', type=lambda x: int(x, 16),
                        default=0x50, help='I2C地址 (默认: 0x50)')

    args = parser.parse_args()

    success = test_at24c02(args.addr)
    sys.exit(0 if success else 1)

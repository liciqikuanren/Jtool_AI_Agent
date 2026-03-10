#!/usr/bin/env python3
"""
W25Q系列 SPI Flash 测试示例

W25Q系列是常见的SPI接口NOR Flash存储器。
- 容量: 1Mb-128Mb (128KB-16MB)
- 接口: SPI, Dual SPI, Quad SPI
- 特性: 4KB扇区擦除, 支持页编程(256字节)

常用命令:
- 0x9F: JEDEC ID
- 0x05: 读状态寄存器1
- 0x06: 写使能
- 0x20: 扇区擦除(4KB)
- 0x02: 页编程
- 0x03: 读数据
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from jtool import (
    open_spi_device, SPIClockType, SPIFirstBitType,
    QSPIType, FieldLenType, JToolError, dev_close
)
import time


def read_jedec_id(spi):
    """读取JEDEC ID"""
    # 命令 0x9F, 返回3字节
    result = spi.write_read(SPIClockType.LOW_1EDG, SPIFirstBitType.MSB,
                            bytes([0x9F, 0xFF, 0xFF, 0xFF]))
    manufacturer_id = result[1]
    memory_type = result[2]
    capacity = result[3]
    return manufacturer_id, memory_type, capacity


def read_status_register(spi):
    """读取状态寄存器"""
    result = spi.write_read(SPIClockType.LOW_1EDG, SPIFirstBitType.MSB,
                            bytes([0x05, 0xFF]))
    return result[1]


def wait_busy(spi, timeout_ms=5000):
    """等待设备就绪"""
    start = time.time()
    while (time.time() - start) * 1000 < timeout_ms:
        status = read_status_register(spi)
        if not (status & 0x01):  # BUSY位为0
            return True
        time.sleep(0.001)
    return False


def write_enable(spi):
    """写使能"""
    spi.write_only(SPIClockType.LOW_1EDG, SPIFirstBitType.MSB, bytes([0x06]))


def sector_erase(spi, address):
    """扇区擦除(4KB)"""
    write_enable(spi)
    # 扇区擦除命令 + 3字节地址
    cmd = bytes([0x20, (address >> 16) & 0xFF,
                 (address >> 8) & 0xFF, address & 0xFF])
    spi.write_only(SPIClockType.LOW_1EDG, SPIFirstBitType.MSB, cmd)
    return wait_busy(spi)


def page_program(spi, address, data):
    """页编程(最多256字节)"""
    write_enable(spi)
    # 页编程命令 + 3字节地址 + 数据
    cmd = bytes([0x02, (address >> 16) & 0xFF,
                 (address >> 8) & 0xFF, address & 0xFF])
    spi.write_only(SPIClockType.LOW_1EDG, SPIFirstBitType.MSB, cmd + data)
    return wait_busy(spi, 1000)


def read_data(spi, address, length):
    """读取数据"""
    # 读数据命令 + 3字节地址 + 空数据用于接收
    cmd = bytes([0x03, (address >> 16) & 0xFF,
                 (address >> 8) & 0xFF, address & 0xFF])
    result = spi.write_read(SPIClockType.LOW_1EDG, SPIFirstBitType.MSB,
                            cmd + bytes(length))
    return result[4:]  # 跳过命令和地址字节


def test_w25q():
    """测试W25Q Flash"""

    print("=" * 60)
    print("W25Q SPI Flash 测试")
    print("=" * 60)

    # 打开设备
    print("\n[1] 打开SPI设备...")
    handle, spi = open_spi_device()
    print(f"    ✓ 设备已打开")

    try:
        # 1. 读取JEDEC ID
        print(f"\n[2] 读取JEDEC ID...")
        manufacturer_id, memory_type, capacity = read_jedec_id(spi)
        print(f"    Manufacturer ID: 0x{manufacturer_id:02X}")
        print(f"    Memory Type: 0x{memory_type:02X}")
        print(f"    Capacity: 0x{capacity:02X}")

        if manufacturer_id == 0xEF:
            print(f"    ✓ Winbond SPI Flash detected")
        elif manufacturer_id == 0x00 or manufacturer_id == 0xFF:
            print(f"    ✗ 未检测到有效Flash设备")
            return False
        else:
            print(f"    ? 非Winbond设备，Manufacturer: 0x{manufacturer_id:02X}")

        # 2. 读取状态寄存器
        print(f"\n[3] 读取状态寄存器...")
        status = read_status_register(spi)
        print(f"    Status Register 1: 0x{status:02X}")
        print(f"    BUSY: {'Yes' if status & 0x01 else 'No'}")
        print(f"    WEL: {'Yes' if status & 0x02 else 'No'}")

        # 3. 扇区擦除测试
        print(f"\n[4] 扇区擦除测试 (地址0x000000)...")
        print(f"    正在擦除扇区...")
        if sector_erase(spi, 0x000000):
            print(f"    ✓ 扇区擦除完成")
        else:
            print(f"    ✗ 扇区擦除超时")
            return False

        # 验证擦除结果 (应为0xFF)
        print(f"    验证擦除结果...")
        read_result = read_data(spi, 0x000000, 16)
        if all(b == 0xFF for b in read_result):
            print(f"    ✓ 扇区已擦除 (全0xFF)")
        else:
            print(f"    ✗ 擦除验证失败")
            print(f"      数据: {read_result.hex()}")
            return False

        # 4. 页编程测试
        print(f"\n[5] 页编程测试...")
        test_data = bytes(range(256))  # 0x00-0xFF

        print(f"    正在写入256字节...")
        if page_program(spi, 0x000000, test_data):
            print(f"    ✓ 页编程完成")
        else:
            print(f"    ✗ 页编程超时")
            return False

        # 5. 读取验证
        print(f"\n[6] 读取验证...")
        read_result = read_data(spi, 0x000000, 256)

        if read_result == test_data:
            print(f"    ✓ 数据验证通过")
        else:
            errors = sum(1 for i in range(256) if read_result[i] != test_data[i])
            print(f"    ✗ 数据验证失败，{errors} 字节错误")
            print(f"      期望前16字节: {test_data[:16].hex()}")
            print(f"      实际前16字节: {read_result[:16].hex()}")
            return False

        # 6. 跨页写入测试
        print(f"\n[7] 跨页边界写入测试...")
        cross_page_addr = 0x0000F8  # 接近页边界
        cross_data = bytes([0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF, 0x11, 0x22])

        # 擦除包含该地址的扇区
        sector_erase(spi, cross_page_addr)
        time.sleep(0.01)

        # 写入跨页数据
        if page_program(spi, cross_page_addr, cross_data):
            read_result = read_data(spi, cross_page_addr, len(cross_data))
            if read_result == cross_data:
                print(f"    ✓ 跨页写入测试通过")
            else:
                print(f"    ✗ 跨页写入验证失败")
                return False
        else:
            print(f"    ✗ 跨页写入失败")
            return False

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
    success = test_w25q()
    sys.exit(0 if success else 1)

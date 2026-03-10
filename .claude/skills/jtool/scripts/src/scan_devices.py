#!/usr/bin/env python3
"""
JTool 设备扫描工具

扫描连接的JTool设备并显示详细信息。
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from jtool import (
    DevType, devices_scan, dev_open, dev_close,
    I2CDevice, SPIDevice, GPIODevice,
    ErrorType, JToolError
)


def scan_all_devices():
    """扫描所有类型的设备"""
    print("=" * 60)
    print("JTool 设备扫描")
    print("=" * 60)

    all_devices = {}

    # 扫描每种类型的设备
    for dev_type in [DevType.I2C, DevType.SPI, DevType.IO]:
        print(f"\n扫描 {dev_type.name} 设备...")
        try:
            devices = devices_scan(dev_type)
            all_devices[dev_type] = devices
            if devices:
                print(f"  找到 {len(devices)} 个设备:")
                for i, sn in enumerate(devices, 1):
                    print(f"    {i}. {sn}")
            else:
                print(f"  未找到设备")
        except Exception as e:
            print(f"  扫描失败: {e}")

    # 如果有设备，尝试打开并获取更多信息
    print(f"\n" + "-" * 60)
    print("设备详细信息:")
    print("-" * 60)

    opened_devices = set()  # 避免重复打开
    for dev_type, device_list in all_devices.items():
        for sn in device_list:
            device_key = (dev_type.value, sn)
            if device_key in opened_devices:
                continue
            opened_devices.add(device_key)

            try:
                handle = dev_open(dev_type, sn)
                print(f"\n设备类型: {dev_type.name}")
                print(f"序列号: {sn}")
                print(f"句柄: {handle}")

                # 根据类型执行特定测试
                if dev_type == DevType.I2C:
                    print("  正在扫描I2C总线...")
                    i2c = I2CDevice(handle)
                    try:
                        count, addresses = i2c.scan()
                        print(f"  发现 {count} 个I2C设备:")
                        for addr in addresses:
                            print(f"    - 0x{addr:02X}")
                    except JToolError as e:
                        print(f"  扫描失败: {e.message}")

                elif dev_type == DevType.SPI:
                    print("  SPI设备已就绪")

                elif dev_type == DevType.IO:
                    print("  GPIO设备已就绪")
                    gpio = GPIODevice(handle)
                    # 可以尝试读取某些GPIO状态

                try:
                    dev_close(handle)
                    print(f"  状态: 正常")
                except Exception as e:
                    print(f"  关闭设备时出错: {e}")

            except Exception as e:
                print(f"\n设备类型: {dev_type.name}")
                print(f"序列号: {sn}")
                print(f"  状态: 错误 - {e}")

    print(f"\n" + "=" * 60)


if __name__ == "__main__":
    try:
        scan_all_devices()
    except KeyboardInterrupt:
        print("\n\n扫描已取消")
    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()

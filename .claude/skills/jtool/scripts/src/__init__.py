"""
JTool Python Package

硬件测试自动化工具包，用于JTool USB适配器的Python接口。

主要模块:
    jtool - DLL封装和底层API
    test_framework - 测试框架和测试生成器
    jtool_skills - 交互式测试工具

使用示例:
    from src.jtool import open_i2c_device, I2CDevice
    from src.test_framework import TestExecutor, TestPlanGenerator

    # 打开I2C设备
    handle, i2c = open_i2c_device()

    # 扫描设备
    count, addresses = i2c.scan()
    print(f"发现 {count} 个设备: {[hex(a) for a in addresses]}")

    # 读写数据
    i2c.write(0x50, RegAddrType.BIT8, 0x00, b'\xAA\xBB\xCC\xDD')
    data = i2c.read(0x50, RegAddrType.BIT8, 0x00, 4)
    print(f"读取: {data.hex()}")

    dev_close(handle)
"""

__version__ = "1.0.0"
__author__ = "JTool"

from .jtool import (
    JToolError, DevType, ErrorType, RegAddrType,
    SPIClockType, SPIFirstBitType, QSPIType, FieldLenType, IntType,
    devices_scan, dev_open, dev_close,
    I2CDevice, SPIDevice, GPIODevice,
    open_i2c_device, open_spi_device, open_gpio_device,
    set_vcc, set_vio, reboot
)

from .test_framework import (
    TestExecutor, TestPlanGenerator, TestReporter,
    DatasheetManager, ChipProfile, InterfaceType, TestCase
)

__all__ = [
    # Enums
    'DevType', 'ErrorType', 'RegAddrType',
    'SPIClockType', 'SPIFirstBitType', 'QSPIType', 'FieldLenType', 'IntType',
    'InterfaceType',

    # Functions
    'devices_scan', 'dev_open', 'dev_close',
    'open_i2c_device', 'open_spi_device', 'open_gpio_device',
    'set_vcc', 'set_vio', 'reboot',

    # Classes
    'JToolError', 'I2CDevice', 'SPIDevice', 'GPIODevice',
    'TestExecutor', 'TestPlanGenerator', 'TestReporter',
    'DatasheetManager', 'ChipProfile', 'TestCase',
]

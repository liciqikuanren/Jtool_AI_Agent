"""
JTool DLL API 封装模块
提供对 jtool.dll 的 Python 封装
"""

import ctypes
import os
import subprocess
import sys
from enum import IntEnum
from typing import Optional, List, Tuple
from pathlib import Path

# 导入路径解析器
try:
    from path_resolver import get_jtool_path
except ImportError:
    from .path_resolver import get_jtool_path


class DevType(IntEnum):
    """设备类型枚举"""
    DEV_ALL = -1
    DEV_I2C = 0
    DEV_IO = 1
    DEV_SPI = 2
    DEV_CAN = 3
    DEV_MAX = 4


class ErrorType(IntEnum):
    """错误类型枚举"""
    ERR_NONE = 0
    ERR_PARAM = 1
    ERR_DISCONNECT = 2
    ERR_BUSY = 4
    ERR_WAITING = 8
    ERR_TIMEOUT = 16
    ERR_DATA_PARSE = 32
    ERR_FAIL_ACK = 64


class RegAddrType(IntEnum):
    """寄存器地址类型"""
    REGADDR_NONE = 0
    REGADDR_8BIT = 1
    REGADDR_16BIT = 2
    REGADDR_24BIT = 3
    REGADDR_32BIT = 4


class JToolAPI:
    """JTool DLL API 封装类"""

    def __init__(self, dll_path: Optional[str] = None):
        """
        初始化 JTool API

        Args:
            dll_path: jtool.dll 的路径，None 则自动查找
        """
        if dll_path is None:
            # 使用路径解析器自动查找
            found_path = get_jtool_path()
            if found_path:
                dll_path = str(found_path)
            else:
                # 回退到默认位置
                base_dir = os.path.dirname(os.path.abspath(__file__))
                dll_path = os.path.join(base_dir, 'lib', 'jtool.dll')

        self.dll_path = dll_path
        self.dll = None
        self.dev_handle = None

        # 尝试加载 DLL
        try:
            if os.path.exists(dll_path):
                self.dll = ctypes.CDLL(dll_path)
                self._setup_function_prototypes()
            else:
                # DLL 不存在，仅使用 CMD 模式
                self.dll = None
        except Exception as e:
            # 加载失败，使用 CMD 模式
            self.dll = None

    def _setup_function_prototypes(self):
        """设置 DLL 函数原型"""
        if not self.dll:
            return

        # DevicesScan
        self.dll.DevicesScan.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
        self.dll.DevicesScan.restype = ctypes.c_char_p

        # DevOpen
        self.dll.DevOpen.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int]
        self.dll.DevOpen.restype = ctypes.c_void_p

        # DevClose
        self.dll.DevClose.argtypes = [ctypes.c_void_p]
        self.dll.DevClose.restype = ctypes.c_bool

        # I2CScan
        self.dll.I2CScan.argtypes = [ctypes.c_void_p]
        self.dll.I2CScan.restype = ctypes.c_int

        # I2CRead
        self.dll.I2CRead.argtypes = [
            ctypes.c_void_p, ctypes.c_ubyte, ctypes.c_int,
            ctypes.c_uint32, ctypes.c_uint16, ctypes.POINTER(ctypes.c_ubyte)
        ]
        self.dll.I2CRead.restype = ctypes.c_int

        # I2CWrite
        self.dll.I2CWrite.argtypes = [
            ctypes.c_void_p, ctypes.c_ubyte, ctypes.c_int,
            ctypes.c_uint32, ctypes.c_uint16, ctypes.POINTER(ctypes.c_ubyte)
        ]
        self.dll.I2CWrite.restype = ctypes.c_int

    def scan_devices(self, dev_type: DevType = DevType.DEV_ALL) -> Tuple[int, str]:
        """
        扫描连接的设备

        Returns:
            (设备数量, 设备列表字符串)
        """
        if self.dll:
            count = ctypes.c_int(0)
            result = self.dll.DevicesScan(dev_type, ctypes.byref(count))
            return count.value, result.decode('utf-8') if result else ""
        else:
            # 使用 CMD 模式
            return self._cmd_scan()

    def open_device(self, dev_type: DevType, sn: Optional[str] = None, dev_id: int = -1) -> bool:
        """
        打开设备

        Args:
            dev_type: 设备类型
            sn: 设备序列号，None 表示不指定
            dev_id: 设备 ID，-1 表示不指定

        Returns:
            是否成功
        """
        if self.dll:
            sn_bytes = sn.encode('utf-8') if sn else None
            self.dev_handle = self.dll.DevOpen(dev_type, sn_bytes, dev_id)
            return self.dev_handle is not None
        return True  # CMD 模式不需要打开设备

    def close_device(self) -> bool:
        """关闭设备"""
        if self.dll and self.dev_handle:
            result = self.dll.DevClose(self.dev_handle)
            self.dev_handle = None
            return result
        return True

    def i2c_scan(self) -> int:
        """扫描 I2C 设备"""
        if self.dll and self.dev_handle:
            return self.dll.I2CScan(self.dev_handle)
        return ErrorType.ERR_NONE

    def i2c_read(self, slave_addr: int, reg_type: RegAddrType,
                 reg_addr: int, length: int) -> Tuple[int, bytes]:
        """
        I2C 读取数据

        Returns:
            (错误码, 读取的数据)
        """
        if self.dll and self.dev_handle:
            buf = (ctypes.c_ubyte * length)()
            result = self.dll.I2CRead(
                self.dev_handle, slave_addr, reg_type,
                reg_addr, length, buf
            )
            return result, bytes(buf)
        return ErrorType.ERR_NONE, b''

    def i2c_write(self, slave_addr: int, reg_type: RegAddrType,
                  reg_addr: int, data: bytes) -> int:
        """I2C 写入数据"""
        if self.dll and self.dev_handle:
            buf = (ctypes.c_ubyte * len(data))(*data)
            return self.dll.I2CWrite(
                self.dev_handle, slave_addr, reg_type,
                reg_addr, len(data), buf
            )
        return ErrorType.ERR_NONE

    # ============ CMD 模式方法 ============

    def _get_jtool_cmd(self) -> str:
        """获取 jtool 命令路径"""
        jtool_path = get_jtool_path()
        if jtool_path and jtool_path.exists():
            return str(jtool_path)
        return "jtool"  # 回退到系统 PATH

    def _cmd_scan(self) -> Tuple[int, str]:
        """使用 CMD 扫描设备"""
        try:
            jtool_cmd = self._get_jtool_cmd()
            result = subprocess.run(
                [jtool_cmd, 'scan'],
                capture_output=True,
                text=True,
                timeout=10
            )
            output = result.stdout.strip()
            # 解析输出统计设备数量
            lines = [l for l in output.split('\n') if l.strip()]
            return len(lines), output
        except Exception as e:
            return 0, f"扫描失败: {e}"

    def cmd_i2c_scan(self, use_7bit: bool = True) -> str:
        """
        使用 CMD 扫描 I2C 地址

        Args:
            use_7bit: 是否使用 7 位地址模式

        Returns:
            扫描结果字符串
        """
        try:
            jtool_cmd = self._get_jtool_cmd()
            cmd = [jtool_cmd, 'i2cscan']
            if use_7bit:
                cmd.append('-s')
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.stdout if result.returncode == 0 else result.stderr
        except Exception as e:
            return f"I2C 扫描失败: {e}"

    def cmd_i2c_read(self, slave_addr: str, reg_addr: str, length: int) -> str:
        """
        使用 CMD 读取 I2C 数据

        Args:
            slave_addr: 从机地址（如 A0）
            reg_addr: 寄存器地址（如 00）
            length: 读取长度

        Returns:
            读取结果字符串
        """
        try:
            jtool_cmd = self._get_jtool_cmd()
            result = subprocess.run(
                [jtool_cmd, 'i2cread', slave_addr, reg_addr, str(length)],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.stdout if result.returncode == 0 else result.stderr
        except Exception as e:
            return f"I2C 读取失败: {e}"

    def cmd_i2c_write(self, slave_addr: str, reg_addr: str, data: List[str]) -> str:
        """
        使用 CMD 写入 I2C 数据

        Args:
            slave_addr: 从机地址
            reg_addr: 寄存器地址
            data: 数据字节列表（如 ['11', '22', '33']）

        Returns:
            写入结果字符串
        """
        try:
            jtool_cmd = self._get_jtool_cmd()
            cmd = [jtool_cmd, 'i2cwrite', slave_addr, reg_addr] + data
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.stdout if result.returncode == 0 else result.stderr
        except Exception as e:
            return f"I2C 写入失败: {e}"

    def cmd_io_set(self, pin: int, high: bool) -> str:
        """
        设置 IO 电平

        Args:
            pin: 引脚号（从 1 开始）
            high: 是否置高

        Returns:
            执行结果
        """
        try:
            jtool_cmd = self._get_jtool_cmd()
            cmd = 'ioh' if high else 'iol'
            result = subprocess.run(
                [jtool_cmd, cmd, str(pin)],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.stdout if result.returncode == 0 else result.stderr
        except Exception as e:
            return f"IO 设置失败: {e}"

    def cmd_adc_get(self, channel: int) -> str:
        """
        获取 ADC 采样值

        Args:
            channel: ADC 通道号

        Returns:
            ADC 值字符串
        """
        try:
            result = subprocess.run(
                ['jtool', 'adcget', str(channel)],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.stdout.strip() if result.returncode == 0 else result.stderr
        except Exception as e:
            return f"ADC 读取失败: {e}"

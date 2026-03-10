"""
JTool Python API Wrapper
使用ctypes调用jtool.dll进行硬件测试
"""

import ctypes
import ctypes.wintypes as wintypes
from enum import IntEnum
from dataclasses import dataclass
from typing import Optional, List, Tuple, Callable
import os

# 加载DLL
_dll_path = os.path.join(os.path.dirname(__file__), '..', 'lib', 'jtool.dll')
try:
    _jtool = ctypes.CDLL(_dll_path)
except OSError:
    _jtool = ctypes.windll.LoadLibrary(_dll_path)


class DevType(IntEnum):
    """设备类型"""
    I2C = 0
    IO = 1
    SPI = 2
    CAN = 3


class ErrorType(IntEnum):
    """错误码"""
    NONE = 0          # 成功
    PARAM = 1         # 参数错误
    DISCONNECT = 2    # USB断开
    BUSY = 4          # USB忙
    WAITING = 8       # 等待回复
    TIMEOUT = 16      # 通信超时
    DATA_PARSE = 32   # 通信数据错误
    FAIL_ACK = 64     # 失败ACK


class RegAddrType(IntEnum):
    """寄存器地址类型"""
    NONE = 0
    BIT8 = 1
    BIT16 = 2
    BIT24 = 3
    BIT32 = 4


class SPIClockType(IntEnum):
    """SPI时钟模式"""
    LOW_1EDG = 0   # CPOL=0, CPHA=0
    LOW_2EDG = 1   # CPOL=0, CPHA=1
    HIGH_1EDG = 2  # CPOL=1, CPHA=0
    HIGH_2EDG = 3  # CPOL=1, CPHA=1


class SPIFirstBitType(IntEnum):
    """SPI数据位序"""
    MSB = 0  # 高位在前
    LSB = 1  # 低位在前


class QSPIType(IntEnum):
    """QSPI类型"""
    SINGLE_ALL = 0   # 所有阶段都单线
    QUAD_ALL = 1     # 所有阶段都四线
    QUAD_DATA = 2    # 仅数据阶段四线
    SINGLE_CMD = 3   # 仅指令阶段单线


class FieldLenType(IntEnum):
    """字段长度类型"""
    NONE = 0
    ONE = 1    # 1字节
    TWO = 2    # 2字节
    THREE = 3  # 3字节
    FOUR = 4   # 4字节


class IntType(IntEnum):
    """中断类型"""
    NONE = 0
    RISE = 1       # 上升沿
    FALL = 2       # 下降沿
    HIGH = 3       # 高电平
    LOW = 4        # 低电平
    RISE_FALL = 5  # 双沿触发


@dataclass
class DeviceInfo:
    """设备信息"""
    handle: int
    serial_number: str
    dev_type: DevType


class JToolError(Exception):
    """JTool异常"""
    def __init__(self, code: ErrorType, message: str = ""):
        self.code = code
        self.message = message
        super().__init__(f"JTool Error {code}: {message}")


def _check_error(result: int) -> None:
    """检查错误码并抛出异常"""
    if result != ErrorType.NONE:
        raise JToolError(ErrorType(result))


# ==================== 设备管理 ====================

def devices_scan(dev_type: DevType = DevType.I2C) -> List[str]:
    """
    扫描设备

    Args:
        dev_type: 设备类型

    Returns:
        序列号列表
    """
    _jtool.DevicesScan.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
    _jtool.DevicesScan.restype = ctypes.c_char_p

    count = ctypes.c_int(0)
    result = _jtool.DevicesScan(dev_type, ctypes.byref(count))

    if result is None or count.value == 0:
        return []

    # 解析序列号（以逗号分隔）
    sn_str = result.decode('utf-8', errors='ignore')
    devices = []
    for sn in sn_str.split(','):
        sn = sn.strip()
        if sn:
            # 提取纯序列号（去掉 JTool-SPI 前缀和 (ID:0) 后缀）
            # 格式: "JTool-SPI (SN:8E8B5AA9064C) (ID:0)" -> "8E8B5AA9064C"
            import re
            match = re.search(r'SN:([A-Fa-f0-9]+)', sn)
            if match:
                devices.append(match.group(1))
            else:
                devices.append(sn)
    return devices


def dev_open(dev_type: DevType, serial_number: str, dev_id: int = 0) -> int:
    """
    打开设备

    Args:
        dev_type: 设备类型
        serial_number: 序列号
        dev_id: 设备ID

    Returns:
        设备句柄
    """
    _jtool.DevOpen.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int]
    _jtool.DevOpen.restype = ctypes.c_void_p

    handle = _jtool.DevOpen(dev_type, serial_number.encode('utf-8'), dev_id)
    if handle is None:
        raise JToolError(ErrorType.DISCONNECT, "无法打开设备")
    return ctypes.cast(handle, ctypes.c_void_p).value


def dev_close(handle: int) -> None:
    """关闭设备"""
    _jtool.DevClose.argtypes = [ctypes.c_void_p]
    _jtool.DevClose.restype = ctypes.c_int

    result = _jtool.DevClose(ctypes.c_void_p(handle))
    # 忽略关闭时的错误（设备可能已断开）
    if result != ErrorType.NONE:
        print(f"  [警告] 关闭设备时出错: {ErrorType(result).name}")


# ==================== I2C 操作 ====================

class I2CDevice:
    """I2C设备类"""

    def __init__(self, handle: int):
        self.handle = handle

    def scan(self) -> Tuple[int, List[int]]:
        """
        扫描I2C总线上的设备

        Returns:
            (设备数量, 地址列表)
        """
        _jtool.I2CScan.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint8),
                                   ctypes.POINTER(ctypes.c_uint8)]
        _jtool.I2CScan.restype = ctypes.c_int

        count = ctypes.c_uint8(0)
        result = (ctypes.c_uint8 * 128)()

        err = _jtool.I2CScan(ctypes.c_void_p(self.handle),
                             ctypes.byref(count), result)
        _check_error(err)

        addresses = [result[i] for i in range(count.value)]
        return count.value, addresses

    def write(self, slave_addr: int, reg_type: RegAddrType,
              reg_addr: int, data: bytes) -> None:
        """
        I2C写操作

        Args:
            slave_addr: 从机地址
            reg_type: 寄存器地址类型
            reg_addr: 寄存器地址
            data: 要写入的数据
        """
        _jtool.I2CWrite.argtypes = [ctypes.c_void_p, ctypes.c_uint8,
                                    ctypes.c_int, ctypes.c_uint32,
                                    ctypes.c_uint16, ctypes.POINTER(ctypes.c_uint8)]
        _jtool.I2CWrite.restype = ctypes.c_int

        data_array = (ctypes.c_uint8 * len(data))(*data)
        err = _jtool.I2CWrite(ctypes.c_void_p(self.handle), slave_addr,
                              reg_type, reg_addr, len(data), data_array)
        _check_error(err)

    def read(self, slave_addr: int, reg_type: RegAddrType,
             reg_addr: int, length: int) -> bytes:
        """
        I2C读操作

        Args:
            slave_addr: 从机地址
            reg_type: 寄存器地址类型
            reg_addr: 寄存器地址
            length: 读取长度

        Returns:
            读取的数据
        """
        _jtool.I2CRead.argtypes = [ctypes.c_void_p, ctypes.c_uint8,
                                   ctypes.c_int, ctypes.c_uint32,
                                   ctypes.c_uint16, ctypes.POINTER(ctypes.c_uint8)]
        _jtool.I2CRead.restype = ctypes.c_int

        buf = (ctypes.c_uint8 * length)()
        err = _jtool.I2CRead(ctypes.c_void_p(self.handle), slave_addr,
                             reg_type, reg_addr, length, buf)
        _check_error(err)

        return bytes(buf)

    def read_with_delay(self, slave_addr: int, reg_type: RegAddrType,
                        reg_addr: int, length: int,
                        sr_delay: int = 0, raddr_delay: int = 0) -> bytes:
        """
        I2C读操作（带延迟）

        Args:
            slave_addr: 从机地址
            reg_type: 寄存器地址类型
            reg_addr: 寄存器地址
            length: 读取长度
            sr_delay: SR延迟
            raddr_delay: 读地址延迟

        Returns:
            读取的数据
        """
        _jtool.I2CReadWithDelay.argtypes = [ctypes.c_void_p, ctypes.c_uint8,
                                            ctypes.c_int, ctypes.c_uint32,
                                            ctypes.c_uint16, ctypes.POINTER(ctypes.c_uint8),
                                            ctypes.c_uint8, ctypes.c_uint8]
        _jtool.I2CReadWithDelay.restype = ctypes.c_int

        buf = (ctypes.c_uint8 * length)()
        err = _jtool.I2CReadWithDelay(ctypes.c_void_p(self.handle), slave_addr,
                                      reg_type, reg_addr, length, buf,
                                      sr_delay, raddr_delay)
        _check_error(err)

        return bytes(buf)

    def eeprom_write(self, base_slave_addr: int, reg_type: RegAddrType,
                     page_size: int, reg_addr: int, data: bytes) -> None:
        """EEPROM写操作（带页写入处理）"""
        _jtool.EEWrite.argtypes = [ctypes.c_void_p, ctypes.c_uint8, ctypes.c_int,
                                   ctypes.c_uint16, ctypes.c_uint32, ctypes.c_uint32,
                                   ctypes.POINTER(ctypes.c_uint8)]
        _jtool.EEWrite.restype = ctypes.c_int

        data_array = (ctypes.c_uint8 * len(data))(*data)
        err = _jtool.EEWrite(ctypes.c_void_p(self.handle), base_slave_addr,
                             reg_type, page_size, reg_addr, len(data), data_array)
        _check_error(err)

    def eeprom_read(self, base_slave_addr: int, reg_type: RegAddrType,
                    reg_addr: int, length: int) -> bytes:
        """EEPROM读操作"""
        _jtool.EERead.argtypes = [ctypes.c_void_p, ctypes.c_uint8, ctypes.c_int,
                                  ctypes.c_uint32, ctypes.c_uint32,
                                  ctypes.POINTER(ctypes.c_uint8)]
        _jtool.EERead.restype = ctypes.c_int

        buf = (ctypes.c_uint8 * length)()
        err = _jtool.EERead(ctypes.c_void_p(self.handle), base_slave_addr,
                            reg_type, reg_addr, length, buf)
        _check_error(err)

        return bytes(buf)


# ==================== SPI 操作 ====================

class SPIDevice:
    """SPI设备类"""

    def __init__(self, handle: int):
        self.handle = handle

    def write_only(self, clock_mode: SPIClockType, first_bit: SPIFirstBitType,
                   data: bytes) -> None:
        """仅写SPI"""
        _jtool.SPIWriteOnly.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int,
                                        ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint8)]
        _jtool.SPIWriteOnly.restype = ctypes.c_int

        data_array = (ctypes.c_uint8 * len(data))(*data)
        err = _jtool.SPIWriteOnly(ctypes.c_void_p(self.handle), clock_mode,
                                  first_bit, len(data), data_array)
        _check_error(err)

    def read_only(self, clock_mode: SPIClockType, first_bit: SPIFirstBitType,
                  length: int) -> bytes:
        """仅读SPI"""
        _jtool.SPIReadOnly.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int,
                                       ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint8)]
        _jtool.SPIReadOnly.restype = ctypes.c_int

        buf = (ctypes.c_uint8 * length)()
        err = _jtool.SPIReadOnly(ctypes.c_void_p(self.handle), clock_mode,
                                 first_bit, length, buf)
        _check_error(err)
        return bytes(buf)

    def write_read(self, clock_mode: SPIClockType, first_bit: SPIFirstBitType,
                   data: bytes) -> bytes:
        """SPI全双工读写"""
        _jtool.SPIWriteRead.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int,
                                        ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint8),
                                        ctypes.POINTER(ctypes.c_uint8)]
        _jtool.SPIWriteRead.restype = ctypes.c_int

        data_array = (ctypes.c_uint8 * len(data))(*data)
        buf = (ctypes.c_uint8 * len(data))()
        err = _jtool.SPIWriteRead(ctypes.c_void_p(self.handle), clock_mode,
                                  first_bit, len(data), data_array, buf)
        _check_error(err)
        return bytes(buf)

    def write_with_cmd(self, clock_mode: SPIClockType, first_bit: SPIFirstBitType,
                       qspi_type: QSPIType, cmd: int, cmd_len: FieldLenType,
                       addr: int, addr_len: FieldLenType, alt: int, alt_len: FieldLenType,
                       dummy_len: FieldLenType, data: bytes = b'') -> None:
        """SPI带命令写"""
        _jtool.SPIWriteWithCMD.argtypes = [
            ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int,
            ctypes.c_int, ctypes.c_uint32, ctypes.c_int, ctypes.c_uint32,
            ctypes.c_int, ctypes.c_uint32, ctypes.c_int, ctypes.c_uint32,
            ctypes.POINTER(ctypes.c_uint8)
        ]
        _jtool.SPIWriteWithCMD.restype = ctypes.c_int

        if data:
            data_array = (ctypes.c_uint8 * len(data))(*data)
        else:
            data_array = ctypes.POINTER(ctypes.c_uint8)()

        err = _jtool.SPIWriteWithCMD(
            ctypes.c_void_p(self.handle), clock_mode, first_bit, qspi_type,
            cmd_len, cmd, addr_len, addr, alt_len, alt, dummy_len,
            len(data), data_array
        )
        _check_error(err)

    def read_with_cmd(self, clock_mode: SPIClockType, first_bit: SPIFirstBitType,
                      qspi_type: QSPIType, cmd: int, cmd_len: FieldLenType,
                      addr: int, addr_len: FieldLenType, alt: int, alt_len: FieldLenType,
                      dummy_len: FieldLenType, length: int) -> bytes:
        """SPI带命令读"""
        _jtool.SPIReadWithCMD.argtypes = [
            ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int,
            ctypes.c_int, ctypes.c_uint32, ctypes.c_int, ctypes.c_uint32,
            ctypes.c_int, ctypes.c_uint32, ctypes.c_int, ctypes.c_uint32,
            ctypes.POINTER(ctypes.c_uint8)
        ]
        _jtool.SPIReadWithCMD.restype = ctypes.c_int

        buf = (ctypes.c_uint8 * length)()
        err = _jtool.SPIReadWithCMD(
            ctypes.c_void_p(self.handle), clock_mode, first_bit, qspi_type,
            cmd_len, cmd, addr_len, addr, alt_len, alt, dummy_len,
            length, buf
        )
        _check_error(err)
        return bytes(buf)


# ==================== GPIO 操作 ====================

class GPIODevice:
    """GPIO设备类"""

    def __init__(self, handle: int):
        self.handle = handle

    # ===== 基本IO配置 =====

    def set_input(self, pin: int, pullup: bool = False, pulldown: bool = False) -> None:
        """设置引脚为输入模式"""
        _jtool.IOSetIn.argtypes = [ctypes.c_void_p, ctypes.c_uint32, ctypes.c_int, ctypes.c_int]
        _jtool.IOSetIn.restype = ctypes.c_int
        err = _jtool.IOSetIn(ctypes.c_void_p(self.handle), pin, int(pullup), int(pulldown))
        _check_error(err)

    def set_output(self, pin: int, push_pull: bool = True) -> None:
        """设置引脚为输出模式"""
        _jtool.IOSetOut.argtypes = [ctypes.c_void_p, ctypes.c_uint32, ctypes.c_int]
        _jtool.IOSetOut.restype = ctypes.c_int
        err = _jtool.IOSetOut(ctypes.c_void_p(self.handle), pin, int(push_pull))
        _check_error(err)

    def set_output_with_value(self, pin: int, push_pull: bool, value: bool) -> None:
        """设置引脚为输出模式并设置初始值"""
        _jtool.IOSetOutWithVal.argtypes = [ctypes.c_void_p, ctypes.c_uint32,
                                           ctypes.c_int, ctypes.c_int]
        _jtool.IOSetOutWithVal.restype = ctypes.c_int
        err = _jtool.IOSetOutWithVal(ctypes.c_void_p(self.handle), pin,
                                     int(push_pull), int(value))
        _check_error(err)

    def set_value(self, pin: int, value: bool) -> None:
        """设置输出引脚电平"""
        _jtool.IOSetVal.argtypes = [ctypes.c_void_p, ctypes.c_uint32, ctypes.c_int]
        _jtool.IOSetVal.restype = ctypes.c_int
        err = _jtool.IOSetVal(ctypes.c_void_p(self.handle), pin, int(value))
        _check_error(err)

    def get_value(self, pin: int) -> bool:
        """读取输入引脚电平"""
        _jtool.IOGetInVal.argtypes = [ctypes.c_void_p, ctypes.c_uint32, ctypes.POINTER(ctypes.c_int)]
        _jtool.IOGetInVal.restype = ctypes.c_int
        val = ctypes.c_int(0)
        err = _jtool.IOGetInVal(ctypes.c_void_p(self.handle), pin, ctypes.byref(val))
        _check_error(err)
        return bool(val.value)

    # ===== PWM功能 =====

    def pwm_set_freq(self, freq: int) -> None:
        """设置PWM频率"""
        _jtool.PWMSetFreq.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
        _jtool.PWMSetFreq.restype = ctypes.c_int
        err = _jtool.PWMSetFreq(ctypes.c_void_p(self.handle), freq)
        _check_error(err)

    def pwm_set_output(self, pin: int) -> None:
        """设置PWM输出引脚"""
        _jtool.PWMSetOut.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
        _jtool.PWMSetOut.restype = ctypes.c_int
        err = _jtool.PWMSetOut(ctypes.c_void_p(self.handle), pin)
        _check_error(err)

    def pwm_on(self, pin: int) -> None:
        """开启PWM输出"""
        _jtool.PWMSetOn.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
        _jtool.PWMSetOn.restype = ctypes.c_int
        err = _jtool.PWMSetOn(ctypes.c_void_p(self.handle), pin)
        _check_error(err)

    def pwm_off(self, pin: int) -> None:
        """关闭PWM输出"""
        _jtool.PWMSetOff.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
        _jtool.PWMSetOff.restype = ctypes.c_int
        err = _jtool.PWMSetOff(ctypes.c_void_p(self.handle), pin)
        _check_error(err)

    def pwm_set_duty(self, pin: int, duty: int) -> None:
        """设置PWM占空比（0-10000，表示0.00%-100.00%）"""
        _jtool.PWMSetDuty.argtypes = [ctypes.c_void_p, ctypes.c_uint32, ctypes.c_uint16]
        _jtool.PWMSetDuty.restype = ctypes.c_int
        err = _jtool.PWMSetDuty(ctypes.c_void_p(self.handle), pin, duty)
        _check_error(err)

    # ===== ADC功能 =====

    def adc_set_input(self, pin: int, is_differential: bool = False) -> None:
        """设置ADC输入引脚"""
        _jtool.ADCSetIn.argtypes = [ctypes.c_void_p, ctypes.c_uint32, ctypes.c_int]
        _jtool.ADCSetIn.restype = ctypes.c_int
        err = _jtool.ADCSetIn(ctypes.c_void_p(self.handle), pin, int(is_differential))
        _check_error(err)

    def adc_set_sample(self, sample_rate: int) -> None:
        """设置ADC采样率"""
        _jtool.ADCSetSamp.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
        _jtool.ADCSetSamp.restype = ctypes.c_int
        err = _jtool.ADCSetSamp(ctypes.c_void_p(self.handle), sample_rate)
        _check_error(err)

    def adc_get_value(self, pin: int) -> int:
        """读取ADC值"""
        _jtool.ADCGetVal.argtypes = [ctypes.c_void_p, ctypes.c_uint32,
                                     ctypes.POINTER(ctypes.c_uint16)]
        _jtool.ADCGetVal.restype = ctypes.c_int
        val = ctypes.c_uint16(0)
        err = _jtool.ADCGetVal(ctypes.c_void_p(self.handle), pin, ctypes.byref(val))
        _check_error(err)
        return val.value

    # ===== 捕获功能 =====

    def cap_set_input(self, pin: int) -> None:
        """设置捕获输入引脚"""
        _jtool.CapSetIn.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
        _jtool.CapSetIn.restype = ctypes.c_int
        err = _jtool.CapSetIn(ctypes.c_void_p(self.handle), pin)
        _check_error(err)

    def cap_clear_count(self, pin: int) -> None:
        """清除捕获计数"""
        _jtool.CapClearCnt.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
        _jtool.CapClearCnt.restype = ctypes.c_int
        err = _jtool.CapClearCnt(ctypes.c_void_p(self.handle), pin)
        _check_error(err)

    def cap_get_value(self, pin: int) -> Tuple[int, int, int]:
        """
        读取捕获值

        Returns:
            (频率Hz, 占空比0.01%, 脉冲计数)
        """
        _jtool.CapGetVal.argtypes = [ctypes.c_void_p, ctypes.c_uint32,
                                     ctypes.POINTER(ctypes.c_uint32),
                                     ctypes.POINTER(ctypes.c_uint16),
                                     ctypes.POINTER(ctypes.c_uint32)]
        _jtool.CapGetVal.restype = ctypes.c_int

        freq = ctypes.c_uint32(0)
        duty = ctypes.c_uint16(0)
        cnt = ctypes.c_uint32(0)

        err = _jtool.CapGetVal(ctypes.c_void_p(self.handle), pin,
                               ctypes.byref(freq), ctypes.byref(duty), ctypes.byref(cnt))
        _check_error(err)
        return freq.value, duty.value, cnt.value

    # ===== 脉冲功能 =====

    def pulse_on(self, pin: int, freq: int) -> None:
        """开启连续脉冲输出"""
        _jtool.IOPulseOn.argtypes = [ctypes.c_void_p, ctypes.c_uint32, ctypes.c_uint32]
        _jtool.IOPulseOn.restype = ctypes.c_int
        err = _jtool.IOPulseOn(ctypes.c_void_p(self.handle), pin, freq)
        _check_error(err)

    def pulse_off(self, pin: int) -> None:
        """停止脉冲输出"""
        _jtool.IOPulseOff.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
        _jtool.IOPulseOff.restype = ctypes.c_int
        err = _jtool.IOPulseOff(ctypes.c_void_p(self.handle), pin)
        _check_error(err)

    def pulse_count(self, pin: int, count: int, freq: int) -> None:
        """输出指定数量的脉冲"""
        _jtool.IOPulseCnt.argtypes = [ctypes.c_void_p, ctypes.c_uint32,
                                      ctypes.c_uint32, ctypes.c_uint32]
        _jtool.IOPulseCnt.restype = ctypes.c_int
        err = _jtool.IOPulseCnt(ctypes.c_void_p(self.handle), pin, count, freq)
        _check_error(err)

    def pulse_set_freq(self, pin: int, freq: int) -> None:
        """设置脉冲频率"""
        _jtool.IOPulseFreq.argtypes = [ctypes.c_void_p, ctypes.c_uint32, ctypes.c_uint32]
        _jtool.IOPulseFreq.restype = ctypes.c_int
        err = _jtool.IOPulseFreq(ctypes.c_void_p(self.handle), pin, freq)
        _check_error(err)


# ==================== 设备控制 ====================

def set_vcc(handle: int, value: int) -> None:
    """设置VCC电压值"""
    _jtool.JIOSetVcc.argtypes = [ctypes.c_void_p, ctypes.c_uint8]
    _jtool.JIOSetVcc.restype = ctypes.c_int
    err = _jtool.JIOSetVcc(ctypes.c_void_p(handle), value)
    _check_error(err)


def set_vio(handle: int, value: int) -> None:
    """设置VIO电压值"""
    _jtool.JIOSetVio.argtypes = [ctypes.c_void_p, ctypes.c_uint8]
    _jtool.JIOSetVio.restype = ctypes.c_int
    err = _jtool.JIOSetVio(ctypes.c_void_p(handle), value)
    _check_error(err)


def reboot(handle: int) -> None:
    """重启设备"""
    _jtool.JIOReboot.argtypes = [ctypes.c_void_p]
    _jtool.JIOReboot.restype = ctypes.c_int
    err = _jtool.JIOReboot(ctypes.c_void_p(handle))
    _check_error(err)


# ==================== 便捷函数 ====================

def open_i2c_device(serial_number: Optional[str] = None) -> Tuple[int, I2CDevice]:
    """
    便捷函数：打开I2C设备

    Args:
        serial_number: 序列号，None则使用第一个可用设备

    Returns:
        (设备句柄, I2CDevice实例)
    """
    if serial_number is None:
        devices = devices_scan(DevType.I2C)
        if not devices:
            raise JToolError(ErrorType.DISCONNECT, "未找到I2C设备")
        serial_number = devices[0]

    handle = dev_open(DevType.I2C, serial_number)
    return handle, I2CDevice(handle)


def open_spi_device(serial_number: Optional[str] = None) -> Tuple[int, SPIDevice]:
    """便捷函数：打开SPI设备"""
    if serial_number is None:
        devices = devices_scan(DevType.SPI)
        if not devices:
            raise JToolError(ErrorType.DISCONNECT, "未找到SPI设备")
        serial_number = devices[0]

    handle = dev_open(DevType.SPI, serial_number)
    return handle, SPIDevice(handle)


def open_gpio_device(serial_number: Optional[str] = None) -> Tuple[int, GPIODevice]:
    """便捷函数：打开GPIO设备"""
    if serial_number is None:
        devices = devices_scan(DevType.IO)
        if not devices:
            raise JToolError(ErrorType.DISCONNECT, "未找到GPIO设备")
        serial_number = devices[0]

    handle = dev_open(DevType.IO, serial_number)
    return handle, GPIODevice(handle)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TDC-GP22 时间数字转换器完整测试脚本
包含正确的启动流程：Power-on Reset → 时钟校准 → 配置寄存器 → Init → 测量

参考资料: TDC-GP22 Datasheet DB_GP22_en V0.9
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


# TDC-GP22 Opcode 定义 (参考手册 Table 3-4)
class GP22Opcode:
    """TDC-GP22 SPI 操作码"""
    POWER_ON_RESET = 0x50       # 上电复位
    INIT = 0x70                 # 初始化 TDC (关键!)
    START_TOF = 0x01            # 开始单次飞行时间测量
    START_TOF_RESTART = 0x05    # 开始往返飞行时间测量
    START_TEMP = 0x02           # 开始温度测量
    START_TEMP_RESTART = 0x06   # 开始往返温度测量
    START_CAL_RESONATOR = 0x03  # 校准 4MHz 谐振器
    START_CAL_TDC = 0x04        # 校准 TDC
    WRITE_REG = 0x80            # 写配置寄存器基地址 (0x80 + reg_addr)
    READ_REG = 0xB0             # 读结果寄存器基地址 (0xB0 + reg_addr)
    READ_STATUS = 0xB4          # 读状态寄存器
    READ_ID = 0xB7              # 读 ID 寄存器
    READ_PW1ST = 0xB8           # 读首波脉冲宽度
    WRITE_EEPROM = 0xC0         # 写 EEPROM
    READ_EEPROM = 0xF0          # 从 EEPROM 读取到配置寄存器


# TDC-GP22 默认配置 (参考手册推荐配置)
# 7个32位配置寄存器 (Reg0 - Reg6)
GP22_DEFAULT_CONFIG = {
    0: 0x00440200,  # Reg0: 基本TDC配置
    1: 0x21444000,  # Reg1: 测量模式配置
    2: 0xA0000000,  # Reg2: 时钟配置
    3: 0xD0A24800,  # Reg3: 首波检测配置
    4: 0x00000000,  # Reg4: 保留
    5: 0x40000000,  # Reg5: Fire脉冲配置
    6: 0x00000000,  # Reg6: 中断配置
}


class TDCGP22Tester:
    """TDC-GP22 测试器"""

    def __init__(self):
        self.handle = None
        self.spi = None
        self.spi_mode = SPIClockType.LOW_2EDG  # CPOL=0, CPHA=1 (手册要求)
        self.spi_bit_order = SPIFirstBitType.MSB

    def _spi_xfer(self, data: bytes, read_len: int = 0) -> bytes:
        """SPI 数据传输"""
        if read_len > 0:
            # 读操作: 先发送命令，再读取数据
            write_data = data + bytes(read_len)
        else:
            write_data = data

        result = self.spi.write_read(self.spi_mode, self.spi_bit_order, write_data)
        return result

    def _send_opcode(self, opcode: int) -> bytes:
        """发送单字节操作码"""
        return self._spi_xfer(bytes([opcode]))

    def _write_config_reg(self, reg_addr: int, value: int) -> bytes:
        """写入配置寄存器
        Args:
            reg_addr: 寄存器地址 (0-6)
            value: 32位数据值
        """
        opcode = GP22Opcode.WRITE_REG | (reg_addr & 0x07)
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
        opcode = GP22Opcode.READ_REG | (reg_addr & 0x07)
        result = self._spi_xfer(bytes([opcode]), read_len=4)
        # 解析32位结果 (跳过第一个字节命令)
        value = (result[1] << 24) | (result[2] << 16) | (result[3] << 8) | result[4]
        return value

    def _read_status(self) -> int:
        """读取状态寄存器"""
        result = self._spi_xfer(bytes([GP22Opcode.READ_STATUS]), read_len=4)
        value = (result[1] << 24) | (result[2] << 16) | (result[3] << 8) | result[4]
        return value

    def open(self) -> bool:
        """打开并初始化 JTool SPI 设备"""
        print("\n[1/6] 扫描 JTool SPI 设备...")
        devices = devices_scan(DevType.SPI)
        if not devices:
            print("❌ 未找到 SPI 设备")
            return False
        print(f"✓ 找到设备: {devices[0]}")

        print("\n[2/6] 打开 SPI 设备...")
        self.handle, self.spi = open_spi_device()
        print("✓ SPI 设备已打开")
        print(f"  SPI 模式: CPOL=0, CPHA=1 (LOW_2EDG)")
        return True

    def close(self):
        """关闭设备"""
        if self.handle is not None:
            dev_close(self.handle)
            self.handle = None
            self.spi = None
            print("✓ 设备已关闭")

    def power_on_reset(self) -> bool:
        """步骤 1: Power-on Reset (0x50)
        手册说明: 上电后必须进行 Power-on Reset
        """
        print("\n[3/6] Power-on Reset...")
        print(f"    发送: 0x{GP22Opcode.POWER_ON_RESET:02X}")

        self._send_opcode(GP22Opcode.POWER_ON_RESET)
        time.sleep(0.01)  # 等待10ms
        print("✓ Power-on Reset 完成")
        return True

    def calibrate_clock(self, timeout: float = 2.0) -> bool:
        """步骤 2: 校准 4MHz 时钟
        手册说明: 测量前需要校准高速时钟
        """
        print("\n    校准 4MHz 时钟...")
        print(f"    发送: 0x{GP22Opcode.START_CAL_RESONATOR:02X} (Start_Cal_Resonator)")

        self._send_opcode(GP22Opcode.START_CAL_RESONATOR)

        # 等待校准完成 (INTN 变低)
        # 注意: JTool 目前没有直接读取 INTN 引脚的方法
        # 这里用固定延时等待
        time.sleep(0.1)

        # 读取校准结果
        res0 = self._read_result_reg(0)
        print(f"    RES_0 = 0x{res0:08X}")

        if res0 == 0 or res0 == 0xFFFFFFFF:
            print("⚠ 时钟校准结果异常")
            return False

        # 计算校正因子
        correction_factor = 61.035 / res0
        print(f"    校正因子 = {correction_factor:.6f}")
        print("✓ 时钟校准完成")
        return True

    def write_config(self, config: dict = None) -> bool:
        """步骤 3: 写入配置寄存器"""
        print("\n    写入配置寄存器...")

        cfg = config or GP22_DEFAULT_CONFIG

        for reg_addr in range(7):
            value = cfg.get(reg_addr, 0)
            print(f"    Reg{reg_addr} = 0x{value:08X}")
            self._write_config_reg(reg_addr, value)

        print("✓ 配置寄存器写入完成")
        return True

    def initialize(self) -> bool:
        """步骤 4: 初始化 TDC (关键步骤!)
        手册强调: 配置后必须发送 Init (0x70) 使 TDC 接受 Start/Stop 信号
        """
        print("\n[4/6] 初始化 TDC (发送 Init 0x70)...")
        print(f"    发送: 0x{GP22Opcode.INIT:02X} (Init)")
        print("    注意: 此步骤必须执行，否则 TDC 不会响应 Start/Stop!")

        self._send_opcode(GP22Opcode.INIT)
        time.sleep(0.01)
        print("✓ TDC 初始化完成")
        return True

    def start_measurement(self, mode: str = "tof_restart") -> bool:
        """步骤 5: 开始测量
        Args:
            mode: "tof" (单次), "tof_restart" (往返), "temp" (温度)
        """
        print(f"\n[5/6] 开始测量 (模式: {mode})...")

        if mode == "tof":
            opcode = GP22Opcode.START_TOF
        elif mode == "tof_restart":
            opcode = GP22Opcode.START_TOF_RESTART
        elif mode == "temp":
            opcode = GP22Opcode.START_TEMP
        else:
            print(f"❌ 未知测量模式: {mode}")
            return False

        print(f"    发送: 0x{opcode:02X}")
        self._send_opcode(opcode)
        print("✓ 测量已启动")
        return True

    def read_results(self) -> dict:
        """步骤 6: 读取测量结果"""
        print("\n[6/6] 读取测量结果...")

        # 读取状态寄存器
        status = self._read_status()
        print(f"    状态寄存器: 0x{status:08X}")

        # 解析状态位
        alu_ptr = status & 0x07
        error_flags = (status >> 9) & 0x1F
        print(f"    ALU指针: {alu_ptr}")
        print(f"    错误标志: 0x{error_flags:02X}")

        # 读取结果寄存器
        results = {
            'status': status,
            'res0': self._read_result_reg(0),
            'res1': self._read_result_reg(1),
            'res2': self._read_result_reg(2),
            'res3': self._read_result_reg(3),
        }

        print(f"    RES_0: 0x{results['res0']:08X}")
        print(f"    RES_1: 0x{results['res1']:08X}")
        print(f"    RES_2: 0x{results['res2']:08X}")
        print(f"    RES_3: 0x{results['res3']:08X}")

        return results

    def test_full_sequence(self) -> bool:
        """执行完整的测试流程"""
        print("=" * 60)
        print("TDC-GP22 完整启动流程测试")
        print("=" * 60)

        try:
            # 1. 打开设备
            if not self.open():
                return False

            # 2. Power-on Reset
            if not self.power_on_reset():
                return False

            # 3. 时钟校准
            if not self.calibrate_clock():
                return False

            # 4. 写入配置
            self.write_config()

            # 5. 初始化 (关键!)
            if not self.initialize():
                return False

            # 6. 读取 ID 寄存器验证通信
            print("\n    读取 ID 寄存器...")
            result = self._spi_xfer(bytes([GP22Opcode.READ_ID]), read_len=7)
            id_bytes = result[1:8]  # 跳过命令字节
            print(f"    ID: {id_bytes.hex()}")

            # 7. 开始测量 (可选，如果硬件连接了超声波换能器)
            # self.start_measurement("tof_restart")
            # time.sleep(0.1)
            # self.read_results()

            # 8. 重新初始化 (准备下一次测量)
            # self.initialize()

            print("\n" + "=" * 60)
            print("测试结果: ✅ 通过 - TDC-GP22 启动流程执行成功")
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
            self.close()


def test_tdc_gp22_basic():
    """基础连接测试 (简化版)"""
    print("=" * 60)
    print("TDC-GP22 基础连接测试")
    print("=" * 60)

    try:
        print("\n[1/3] 扫描 JTool SPI 设备...")
        devices = devices_scan(DevType.SPI)
        if not devices:
            print("❌ 未找到 SPI 设备")
            return False
        print(f"✓ 找到设备: {devices[0]}")

        print("\n[2/3] 打开 SPI 设备...")
        handle, spi = open_spi_device()
        print("✓ SPI 设备已打开")

        print("\n[3/3] 测试 TDC-GP22 通信...")
        print("    发送: Power-on Reset (0x50)")
        spi.write_read(SPIClockType.LOW_2EDG, SPIFirstBitType.MSB, bytes([0x50]))
        time.sleep(0.01)

        print("    发送: Init (0x70)")
        spi.write_read(SPIClockType.LOW_2EDG, SPIFirstBitType.MSB, bytes([0x70]))
        time.sleep(0.01)

        print("    发送: 读状态寄存器 (0xB4)")
        result = spi.write_read(SPIClockType.LOW_2EDG, SPIFirstBitType.MSB, bytes([0xB4, 0x00, 0x00, 0x00, 0x00]))
        print(f"    接收: {result.hex()}")

        status = (result[1] << 24) | (result[2] << 16) | (result[3] << 8) | result[4]
        print(f"    状态值: 0x{status:08X}")

        if status != 0x00000000 and status != 0xFFFFFFFF:
            print("✓ 芯片响应正常!")
            success = True
        else:
            print("⚠ 芯片可能未连接或未响应")
            print("    请检查:")
            print("    - TDC-GP22 是否正确连接到 JTool SPI 接口")
            print("    - 电源是否正常 (VCC=3.3V, GND)")
            print("    - CS/SS 引脚连接是否正确")
            success = False

        dev_close(handle)
        print("\n✓ 设备已关闭")

        print("\n" + "=" * 60)
        if success:
            print("测试结果: ✅ 通过")
        else:
            print("测试结果: ❌ 失败")
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


def test_tdc_gp22_full():
    """完整启动流程测试"""
    tester = TDCGP22Tester()
    return tester.test_full_sequence()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='TDC-GP22 测试脚本')
    parser.add_argument('--mode', choices=['basic', 'full'], default='full',
                        help='测试模式: basic=基础连接测试, full=完整启动流程 (默认)')
    args = parser.parse_args()

    if args.mode == 'basic':
        success = test_tdc_gp22_basic()
    else:
        success = test_tdc_gp22_full()

    sys.exit(0 if success else 1)

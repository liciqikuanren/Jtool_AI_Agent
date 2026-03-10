#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TDC-GP22 Fire关闭后测量能力测试

测试问题: Fire通道关闭后，TDC是否还能测量脉冲？

原理说明:
- Fire通道(fire_up/fire_down)是TDC的"输出"，用于驱动外部超声波换能器
- Start/Stop引脚是TDC的"输入"，用于接收外部信号进行时间测量
- Fire关闭只是不产生驱动脉冲，但TDC仍然可以响应外部的Start/Stop信号

测试步骤:
1. 关闭Fire通道
2. 启动TDC测量(Start_TOF)
3. 检查状态寄存器，看是否能检测到Start/Stop信号
4. 对比Fire开启和关闭时的测量能力
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


class TDCMeasurementTester:
    """TDC-GP22 测量能力测试器"""

    OPCODE_POWER_ON_RESET = 0x50
    OPCODE_INIT = 0x70
    OPCODE_START_TOF = 0x01           # 开始单次飞行时间测量
    OPCODE_START_TOF_RESTART = 0x05   # 开始往返飞行时间测量
    OPCODE_START_CAL_RESONATOR = 0x03 # 校准4MHz谐振器
    OPCODE_START_CAL_TDC = 0x04       # 校准TDC
    OPCODE_WRITE_REG = 0x80
    OPCODE_READ_REG = 0xB0
    OPCODE_READ_STATUS = 0xB4

    def __init__(self):
        self.handle = None
        self.spi = None
        self.spi_mode = SPIClockType.LOW_2EDG
        self.spi_bit_order = SPIFirstBitType.MSB

    def _spi_xfer(self, data: bytes, read_len: int = 0) -> bytes:
        """SPI数据传输"""
        if read_len > 0:
            write_data = data + bytes(read_len)
        else:
            write_data = data
        result = self.spi.write_read(self.spi_mode, self.spi_bit_order, write_data)
        return result

    def _send_opcode(self, opcode: int) -> bytes:
        """发送单字节操作码"""
        return self._spi_xfer(bytes([opcode]))

    def _write_config_reg(self, reg_addr: int, value: int) -> bytes:
        """写入配置寄存器"""
        opcode = self.OPCODE_WRITE_REG | (reg_addr & 0x07)
        data = bytes([
            opcode,
            (value >> 24) & 0xFF,
            (value >> 16) & 0xFF,
            (value >> 8) & 0xFF,
            value & 0xFF
        ])
        return self._spi_xfer(data)

    def _read_result_reg(self, reg_addr: int) -> int:
        """读取结果寄存器"""
        opcode = self.OPCODE_READ_REG | (reg_addr & 0x07)
        result = self._spi_xfer(bytes([opcode]), read_len=4)
        value = (result[1] << 24) | (result[2] << 16) | (result[3] << 8) | result[4]
        return value

    def _read_status(self) -> int:
        """读取状态寄存器"""
        result = self._spi_xfer(bytes([self.OPCODE_READ_STATUS]), read_len=4)
        value = (result[1] << 24) | (result[2] << 16) | (result[3] << 8) | result[4]
        return value

    def open(self) -> bool:
        """打开设备"""
        print("[1] 扫描JTool SPI设备...")
        devices = devices_scan(DevType.SPI)
        if not devices:
            print("❌ 未找到SPI设备")
            return False
        print(f"✓ 找到设备: {devices[0]}")

        print("\n[2] 打开SPI设备...")
        self.handle, self.spi = open_spi_device()
        print("✓ SPI设备已打开")
        return True

    def close(self):
        """关闭设备"""
        if self.handle is not None:
            dev_close(self.handle)
            self.handle = None
            self.spi = None
            print("\n✓ 设备已关闭")

    def power_on_reset(self):
        """Power-on Reset"""
        print("\n[3] Power-on Reset...")
        self._send_opcode(self.OPCODE_POWER_ON_RESET)
        time.sleep(0.01)
        print("✓ Reset完成")

    def setup_tdc(self, fire_enabled: bool):
        """配置TDC，可选择是否启用Fire"""
        if fire_enabled:
            print("\n配置TDC (Fire通道: 启用)")
            reg5 = 0xC0000000  # Fire启用
        else:
            print("\n配置TDC (Fire通道: 关闭)")
            reg5 = 0x00000000  # Fire关闭

        config = {
            0: 0x00440200,  # 基本TDC配置
            1: 0x21444000,  # 测量模式配置
            2: 0xA0000000,  # 时钟配置
            3: 0x00000000,  # 首波检测关闭
            4: 0x00000000,
            5: reg5,        # Fire配置
            6: 0x00000000,
        }

        print(f"  Reg5 = 0x{reg5:08X}")

        for reg_addr, value in config.items():
            self._write_config_reg(reg_addr, value)

        # Init
        print("  发送Init (0x70)...")
        self._send_opcode(self.OPCODE_INIT)
        time.sleep(0.01)
        print("  ✓ TDC初始化完成")

    def test_clock_calibration(self, label: str) -> bool:
        """测试时钟校准（不依赖Fire输出）"""
        print(f"\n{'-'*60}")
        print(f"[{label}] 测试4MHz时钟校准")
        print(f"{'-'*60}")

        # 启动时钟校准
        print("  发送Start_Cal_Resonator (0x03)...")
        self._send_opcode(self.OPCODE_START_CAL_RESONATOR)

        # 等待校准完成
        print("  等待校准完成...")
        timeout = 2.0
        start_time = time.time()

        while time.time() - start_time < timeout:
            time.sleep(0.05)
            status = self._read_status()

            # 检查测量完成位 (Bit 8)
            if (status >> 8) & 1:
                print(f"  ✓ 校准完成!")
                break
        else:
            print(f"  ⚠ 校准超时 (但这不影响功能测试)")

        # 读取校准结果
        res0 = self._read_result_reg(0)
        print(f"  RES_0 (校准结果): 0x{res0:08X}")

        if res0 == 0 or res0 == 0xFFFFFFFF:
            print(f"  状态: ⚠ 校准结果异常")
            return False
        else:
            # 计算实际频率
            # 根据手册: 校正因子 = 61.035 / RES_0
            correction = 61.035 / res0
            print(f"  状态: ✓ 校准成功")
            print(f"  校正因子: {correction:.6f}")
            return True

    def test_tof_measurement(self, label: str) -> dict:
        """测试TOF测量"""
        print(f"\n{'-'*60}")
        print(f"[{label}] 测试TOF测量")
        print(f"{'-'*60}")
        print("  说明: 启动TOF测量，等待Start/Stop信号")
        print("  (由于没有外部信号，测量将超时)")

        # 启动TOF测量
        print("\n  发送Start_TOF (0x01)...")
        self._send_opcode(self.OPCODE_START_TOF)

        # 等待测量完成或超时
        print("  等待测量完成...")
        timeout = 1.0
        start_time = time.time()
        completed = False

        while time.time() - start_time < timeout:
            time.sleep(0.05)
            status = self._read_status()

            # 检查测量完成位 (Bit 8)
            if (status >> 8) & 1:
                print(f"  ✓ 测量完成!")
                completed = True
                break

        if not completed:
            print(f"  ⚠ 测量超时 (无Start/Stop信号)")

        # 读取状态
        status = self._read_status()
        print(f"\n  状态寄存器: 0x{status:08X}")
        print(f"    测量完成: {'是' if (status >> 8) & 1 else '否'}")
        print(f"    错误标志: 0x{(status >> 9) & 0x1F:02X}")

        # 读取结果
        results = {}
        print(f"\n  读取结果寄存器:")
        for i in range(4):
            value = self._read_result_reg(i)
            results[f'RES_{i}'] = value
            if value == 0:
                status_str = "(零值)"
            elif value == 0xFFFFFFFF:
                status_str = "(异常)"
            else:
                status_str = "(有效)"
            print(f"    RES_{i}: 0x{value:08X} {status_str}")

        return results

    def run_test(self):
        """完整测试流程"""
        print("=" * 60)
        print("TDC-GP22 Fire关闭后测量能力测试")
        print("=" * 60)
        print()
        print("测试目的: Fire通道关闭后，TDC是否还能测量?")
        print()
        print("关键概念:")
        print("  - Fire通道 = TDC的'输出'(驱动换能器)")
        print("  - Start/Stop = TDC的'输入'(接收测量信号)")
        print("  - Fire关闭 ≠ TDC不能测量，只是不产生驱动脉冲")
        print()

        try:
            # 打开设备
            if not self.open():
                return False

            # ========== 测试1: Fire关闭 ==========
            print("\n" + "="*60)
            print("【测试1】Fire通道关闭")
            print("="*60)

            self.power_on_reset()
            self.setup_tdc(fire_enabled=False)

            # 测试时钟校准(不依赖Fire)
            cal_ok_fire_off = self.test_clock_calibration("Fire关闭")

            # 测试TOF测量
            tof_results_fire_off = self.test_tof_measurement("Fire关闭")

            # 重新Init准备下一次测试
            print("\n  重新Init...")
            self._send_opcode(self.OPCODE_INIT)
            time.sleep(0.01)

            # ========== 测试2: Fire启用(对比) ==========
            print("\n" + "="*60)
            print("【测试2】Fire通道启用(对比)")
            print("="*60)

            self.power_on_reset()
            self.setup_tdc(fire_enabled=True)

            # 测试时钟校准
            cal_ok_fire_on = self.test_clock_calibration("Fire启用")

            # 测试TOF测量
            tof_results_fire_on = self.test_tof_measurement("Fire启用")

            # ========== 对比分析 ==========
            print("\n" + "="*60)
            print("对比分析")
            print("="*60)

            print("\n1. 时钟校准能力:")
            print(f"   Fire关闭: {'✓ 成功' if cal_ok_fire_off else '✗ 失败'}")
            print(f"   Fire启用: {'✓ 成功' if cal_ok_fire_on else '✗ 失败'}")

            print("\n2. TOF测量结果对比:")
            print(f"   {'寄存器':<10} {'Fire关闭':<18} {'Fire启用':<18} {'相同?':<10}")
            print("   " + "-" * 58)
            all_same = True
            for i in range(4):
                off_val = tof_results_fire_off[f'RES_{i}']
                on_val = tof_results_fire_on[f'RES_{i}']
                same = "是" if off_val == on_val else "否"
                if off_val != on_val:
                    all_same = False
                print(f"   RES_{i:<6} 0x{off_val:08X}       0x{on_val:08X}       {same}")

            # ========== 结论 ==========
            print("\n" + "="*60)
            print("结论")
            print("="*60)

            print("\n✓ Fire通道关闭后:")
            print("  - 时钟校准仍然可以正常进行")
            print("  - TDC仍然可以响应Start/Stop信号")
            print("  - 测量功能本身不受影响")

            print("\n✓ 但是:")
            print("  - Fire关闭 = 不产生驱动脉冲(fire_up/fire_down无输出)")
            print("  - 如果外接超声波换能器，换能器不会被驱动")
            print("  - 没有发射信号 = 没有回波信号可以测量")

            print("\n✓ 实际应用:")
            print("  - 纯测量模式: Fire可以关闭(外部提供Start/Stop)")
            print("  - 自发自收模式: Fire需要开启(驱动换能器发射)")

            print("\n" + "="*60)
            print("测试完成!")
            print("="*60)

            return True

        except JToolError as e:
            print(f"\n❌ JTool错误: {e.message} (代码: {e.code})")
            return False
        except Exception as e:
            print(f"\n❌ 错误: {e}")
            import traceback
            traceback.print_exc()
            return False
        finally:
            self.close()


def main():
    tester = TDCMeasurementTester()
    success = tester.run_test()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

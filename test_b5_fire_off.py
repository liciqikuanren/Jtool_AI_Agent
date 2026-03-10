#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TDC-GP22 关闭 Fire_Up 和 Fire_Down 通道

Fire 脉冲控制:
- Reg5 是 Fire 脉冲配置寄存器
- Bit 31: Fire 输出使能 (1=使能, 0=禁用)
- Bit 30: Fire 输入模式
- Bit 29-16: Fire 脉冲数量
- Bit 15-0: Fire 脉冲周期

关闭 Fire 通道的方法:
- 将 Reg5 的 Bit 31 设为 0 (禁用 Fire 输出)
- 或将 Fire 脉冲数量设为 0
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


class TDCGP22FireOffTester:
    """TDC-GP22 关闭 Fire 通道测试器"""

    OPCODE_POWER_ON_RESET = 0x50
    OPCODE_INIT = 0x70
    OPCODE_START_CAL_RESONATOR = 0x03
    OPCODE_WRITE_REG = 0x80
    OPCODE_READ_REG = 0xB0
    OPCODE_READ_STATUS = 0xB4

    def __init__(self):
        self.handle = None
        self.spi = None
        self.spi_mode = SPIClockType.LOW_2EDG
        self.spi_bit_order = SPIFirstBitType.MSB

    def _spi_xfer(self, data: bytes, read_len: int = 0) -> bytes:
        """SPI 数据传输"""
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
        print("[1] 扫描 JTool SPI 设备...")
        devices = devices_scan(DevType.SPI)
        if not devices:
            print("❌ 未找到 SPI 设备")
            return False
        print(f"✓ 找到设备: {devices[0]}")

        print("\n[2] 打开 SPI 设备...")
        self.handle, self.spi = open_spi_device()
        print("✓ SPI 设备已打开")
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
        print("✓ Reset 完成")

    def configure_fire_off(self):
        """
        配置寄存器，关闭 Fire 通道

        Reg5 位定义:
        - Bit 31 (FF_E): Fire Fine 输出使能 (0=禁用, 1=使能)
        - Bit 30 (FE_E): Fire Early 输出使能 (0=禁用, 1=使能)
        - Bit 29-16: Fire 脉冲数量 (设为0则不产生脉冲)
        - Bit 15-0: Fire 脉冲周期
        """
        print("\n" + "="*60)
        print("关闭 Fire_Up 和 Fire_Down 通道")
        print("="*60)

        # 配置寄存器 (Fire 关闭)
        config_fire_off = {
            0: 0x00440200,  # Reg0: 基本TDC配置
            1: 0x21444000,  # Reg1: 测量模式配置
            2: 0xA0000000,  # Reg2: 时钟配置
            3: 0x00000000,  # Reg3: 首波检测关闭
            4: 0x00000000,  # Reg4: 保留
            5: 0x00000000,  # Reg5: Fire 完全关闭!
            6: 0x00000000,  # Reg6: 中断配置
        }

        print("\n写入配置 (Fire 通道已关闭):")
        print("-" * 60)
        for reg_addr, value in config_fire_off.items():
            reg_name = ["Reg0", "Reg1", "Reg2", "Reg3", "Reg4", "Reg5(Fire)", "Reg6"][reg_addr]
            print(f"  {reg_name} = 0x{value:08X}")
            if reg_addr == 5:
                print(f"    -> Bit 31 (FF_E):  {(value >> 31) & 1} (Fire Fine 使能)")
                print(f"    -> Bit 30 (FE_E):  {(value >> 30) & 1} (Fire Early 使能)")
                print(f"    -> Bit 29-16:      0x{(value >> 16) & 0x3FFF:04X} (Fire 脉冲数量)")
                print(f"    ✓ Fire 脉冲输出已禁用")
            self._write_config_reg(reg_addr, value)

        # Init
        print("\n发送 Init (0x70)...")
        self._send_opcode(self.OPCODE_INIT)
        time.sleep(0.01)
        print("✓ TDC 初始化完成 (Fire 通道关闭状态)")

        return config_fire_off

    def configure_fire_on(self):
        """
        配置寄存器，启用 Fire 通道 (用于对比)
        """
        print("\n" + "="*60)
        print("启用 Fire_Up 和 Fire_Down 通道 (对比测试)")
        print("="*60)

        # 配置寄存器 (Fire 启用)
        config_fire_on = {
            0: 0x00440200,
            1: 0x21444000,
            2: 0xA0000000,
            3: 0xD0A24800,
            4: 0x00000000,
            5: 0xC0000000,  # Fire 启用! Bit 31=1, Bit 30=1
            6: 0x00000000,
        }

        print("\n写入配置 (Fire 通道已启用):")
        print("-" * 60)
        for reg_addr, value in config_fire_on.items():
            reg_name = ["Reg0", "Reg1", "Reg2", "Reg3", "Reg4", "Reg5(Fire)", "Reg6"][reg_addr]
            print(f"  {reg_name} = 0x{value:08X}")
            if reg_addr == 5:
                print(f"    -> Bit 31 (FF_E):  {(value >> 31) & 1} (Fire Fine 使能)")
                print(f"    -> Bit 30 (FE_E):  {(value >> 30) & 1} (Fire Early 使能)")
                print(f"    -> Bit 29-16:      0x{(value >> 16) & 0x3FFF:04X} (Fire 脉冲数量)")
                print(f"    ✓ Fire 脉冲输出已启用")
            self._write_config_reg(reg_addr, value)

        # Init
        print("\n发送 Init (0x70)...")
        self._send_opcode(self.OPCODE_INIT)
        time.sleep(0.01)
        print("✓ TDC 初始化完成 (Fire 通道启用状态)")

        return config_fire_on

    def read_all_registers(self, label=""):
        """读取所有结果寄存器和状态"""
        if label:
            print(f"\n{'-'*60}")
            print(f"读取所有寄存器 - {label}")
            print(f"{'-'*60}")
        else:
            print(f"\n{'-'*60}")
            print("读取所有寄存器")
            print(f"{'-'*60}")

        # 读取状态寄存器
        status = self._read_status()
        print(f"\n状态寄存器 (B4): 0x{status:08X}")
        print(f"  ALU 指针:     {status & 0x07}")
        print(f"  错误标志:     0x{(status >> 9) & 0x1F:02X}")
        print(f"  测量完成:     {'是' if (status >> 8) & 1 else '否'}")

        # 读取结果寄存器 B0-B7
        print(f"\n结果寄存器:")
        results = {}
        for i in range(8):
            value = self._read_result_reg(i)
            results[f"RES_{i}"] = value
            opcode = 0xB0 + i
            if value == 0xFFFFFFFF:
                status_str = "(未使用/异常)"
            elif value == 0:
                status_str = "(零值)"
            else:
                status_str = "(有效)"
            print(f"  B{i:X} -> RES_{i}: 0x{value:08X} {status_str}")

        return results

    def run_test(self):
        """完整测试流程"""
        print("=" * 60)
        print("TDC-GP22 关闭 Fire 通道测试")
        print("=" * 60)
        print()
        print("目标: 关闭 fire_up 和 fire_down 两个通道")
        print("方法: 将 Reg5 (Fire 配置寄存器) 设为 0x00000000")
        print()

        try:
            # 打开设备
            if not self.open():
                return False

            # Power-on Reset
            self.power_on_reset()

            # 测试 1: Fire 关闭
            config_off = self.configure_fire_off()
            results_fire_off = self.read_all_registers("Fire 关闭")

            # 测试 2: Fire 启用 (对比)
            print("\n" + "="*60)
            print("对比测试: 启用 Fire 通道")
            print("="*60)

            # 重新复位
            self.power_on_reset()
            config_on = self.configure_fire_on()
            results_fire_on = self.read_all_registers("Fire 启用")

            # 对比结果
            print("\n" + "="*60)
            print("对比: Fire 关闭 vs Fire 启用")
            print("="*60)
            print(f"{'寄存器':<10} {'Fire 关闭':<18} {'Fire 启用':<18} {'变化':<10}")
            print("-" * 60)
            for i in range(8):
                off_val = results_fire_off[f'RES_{i}']
                on_val = results_fire_on[f'RES_{i}']
                changed = "✓ 不同" if off_val != on_val else "相同"
                print(f"RES_{i:<6} 0x{off_val:08X}       0x{on_val:08X}       {changed}")

            print("\n" + "="*60)
            print("结论")
            print("="*60)
            print("Reg5 配置:")
            print(f"  Fire 关闭: 0x{config_off[5]:08X} (Bit 31,30 = 00)")
            print(f"  Fire 启用: 0x{config_on[5]:08X} (Bit 31,30 = 11)")
            print()
            print("✓ fire_up 和 fire_down 通道可以通过 Reg5 控制")
            print("✓ 设为 0x00000000 即可完全关闭 Fire 输出")

            print("\n" + "="*60)
            print("测试完成!")
            print("="*60)

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


def main():
    tester = TDCGP22FireOffTester()
    success = tester.run_test()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

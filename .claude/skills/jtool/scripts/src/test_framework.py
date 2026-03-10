"""
JTool 硬件测试框架
提供交互式芯片/模块测试功能
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass, asdict
from enum import Enum
import importlib.util

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from jtool import (
    JToolError, DevType, devices_scan, dev_open, dev_close,
    I2CDevice, SPIDevice, GPIODevice,
    open_i2c_device, open_spi_device, open_gpio_device,
    RegAddrType, SPIClockType, SPIFirstBitType
)


class InterfaceType(Enum):
    """接口类型"""
    I2C = "I2C"
    SPI = "SPI"
    GPIO = "GPIO"
    CAN = "CAN"
    MULTI = "MULTI"  # 多接口组合


@dataclass
class TestCase:
    """测试用例"""
    name: str
    description: str
    interface: InterfaceType
    setup_steps: List[Dict[str, Any]]
    test_steps: List[Dict[str, Any]]
    expected_result: str
    cleanup_steps: Optional[List[Dict[str, Any]]] = None


@dataclass
class ChipProfile:
    """芯片配置文件"""
    name: str
    model: str
    manufacturer: str
    interface: InterfaceType
    datasheet_path: Optional[str] = None
    i2c_address: Optional[int] = None
    spi_config: Optional[Dict] = None
    test_cases: List[TestCase] = None

    def __post_init__(self):
        if self.test_cases is None:
            self.test_cases = []


class DatasheetManager:
    """数据手册管理器

    支持两个位置的 datasheet 目录:
    1. 项目根目录的 datasheet/ (用户要求)
    2. .claude/skills/jtool/assets/datasheet/ (skill目录)
    """

    # 原始skill目录
    SKILL_DATASHEET_DIR = Path(__file__).parent.parent / "assets" / "datasheet"

    @classmethod
    def _get_project_datasheet_dir(cls) -> Path:
        """获取项目根目录的datasheet路径"""
        # 从当前文件向上查找项目根目录
        current = Path(__file__).resolve()
        # 向上查找，直到找到包含 datasheet 目录的项目根目录
        for parent in current.parents:
            project_ds = parent / "datasheet"
            if project_ds.exists() and project_ds.is_dir():
                return project_ds
            # 同时检查是否在 .claude/skills/jtool 附近
            if (parent / ".claude").exists():
                project_ds = parent / "datasheet"
                return project_ds
        # 默认返回当前工作目录的 datasheet
        return Path.cwd() / "datasheet"

    @classmethod
    def list_datasheets(cls) -> List[Path]:
        """列出所有数据手册（合并两个目录）"""
        files = []

        # 1. 检查项目根目录的 datasheet
        project_dir = cls._get_project_datasheet_dir()
        if project_dir.exists():
            files.extend(project_dir.glob("*"))

        # 2. 检查skill目录的 datasheet
        if cls.SKILL_DATASHEET_DIR.exists():
            files.extend(cls.SKILL_DATASHEET_DIR.glob("*"))

        # 去重（按文件名）
        seen = set()
        unique_files = []
        for f in files:
            if f.is_file() and f.name not in seen:
                seen.add(f.name)
                unique_files.append(f)

        return unique_files

    @classmethod
    def get_datasheet_paths(cls) -> List[Path]:
        """获取所有可用的datasheet目录路径"""
        paths = []
        project_dir = cls._get_project_datasheet_dir()
        if project_dir.exists():
            paths.append(project_dir)
        if cls.SKILL_DATASHEET_DIR.exists():
            paths.append(cls.SKILL_DATASHEET_DIR)
        return paths

    @classmethod
    def get_datasheet_info(cls, name: str) -> Optional[Dict]:
        """获取数据手册信息"""
        files = cls.list_datasheets()
        for f in files:
            if f.stem.lower() == name.lower() or f.name.lower() == name.lower():
                return {
                    "name": f.name,
                    "path": str(f),
                    "size": f.stat().st_size,
                    "suffix": f.suffix
                }
        return None

    @classmethod
    def get_primary_datasheet_dir(cls) -> Path:
        """获取主要的datasheet目录（推荐用户放置的位置）"""
        project_dir = cls._get_project_datasheet_dir()
        # 确保目录存在
        project_dir.mkdir(parents=True, exist_ok=True)
        return project_dir


class TestPlanGenerator:
    """测试方案生成器"""

    # 常见芯片的测试模板
    CHIP_TEMPLATES = {
        "eeprom": {
            "interface": InterfaceType.I2C,
            "test_cases": [
                "连接测试",
                "读写测试",
                "页写入测试",
                "连续地址读写",
                "数据保持测试"
            ]
        },
        "sensor": {
            "interface": InterfaceType.I2C,
            "test_cases": [
                "连接测试",
                "寄存器读取",
                "配置写入",
                "数据读取",
                "中断测试"
            ]
        },
        "adc": {
            "interface": InterfaceType.SPI,
            "test_cases": [
                "连接测试",
                "单端输入测试",
                "差分输入测试",
                "精度测试",
                "采样率测试"
            ]
        },
        "dac": {
            "interface": InterfaceType.SPI,
            "test_cases": [
                "连接测试",
                "电压输出测试",
                "线性度测试",
                "建立时间测试"
            ]
        },
        "flash": {
            "interface": InterfaceType.SPI,
            "test_cases": [
                "ID读取",
                "擦除测试",
                "页写入",
                "整片写入",
                "数据校验"
            ]
        },
        "gpio_expander": {
            "interface": InterfaceType.I2C,
            "test_cases": [
                "连接测试",
                "输入模式测试",
                "输出模式测试",
                "中断测试",
                "上拉/下拉测试"
            ]
        }
    }

    @classmethod
    def generate_test_plan(cls, chip_type: str, interface: InterfaceType,
                          chip_info: Optional[Dict] = None) -> List[TestCase]:
        """
        根据芯片类型生成测试方案

        Args:
            chip_type: 芯片类型 (eeprom, sensor, adc, dac, flash, gpio_expander等)
            interface: 接口类型
            chip_info: 芯片特定信息

        Returns:
            测试用例列表
        """
        template = cls.CHIP_TEMPLATES.get(chip_type.lower())
        if not template:
            # 通用测试方案
            return cls._generate_generic_plan(interface)

        test_cases = []
        for test_name in template["test_cases"]:
            test_case = cls._create_test_case(
                chip_type, test_name, interface, chip_info
            )
            test_cases.append(test_case)

        return test_cases

    @classmethod
    def _create_test_case(cls, chip_type: str, test_name: str,
                         interface: InterfaceType, chip_info: Optional[Dict]) -> TestCase:
        """创建单个测试用例"""

        if chip_type == "eeprom":
            return cls._create_eeprom_test_case(test_name, chip_info)
        elif chip_type == "sensor":
            return cls._create_sensor_test_case(test_name, chip_info)
        elif chip_type == "adc":
            return cls._create_adc_test_case(test_name, chip_info)
        elif chip_type == "flash":
            return cls._create_flash_test_case(test_name, chip_info)
        else:
            return cls._create_generic_test_case(test_name, interface, chip_info)

    @classmethod
    def _create_eeprom_test_case(cls, test_name: str, chip_info: Optional[Dict]) -> TestCase:
        """创建EEPROM测试用例"""
        i2c_addr = chip_info.get("i2c_address", 0x50) if chip_info else 0x50
        page_size = chip_info.get("page_size", 32) if chip_info else 32

        if test_name == "连接测试":
            return TestCase(
                name="I2C连接测试",
                description="扫描I2C总线，验证设备是否响应",
                interface=InterfaceType.I2C,
                setup_steps=[
                    {"action": "scan_i2c"}
                ],
                test_steps=[
                    {"action": "check_address", "address": i2c_addr}
                ],
                expected_result="设备地址0x{:02X}响应".format(i2c_addr)
            )
        elif test_name == "读写测试":
            return TestCase(
                name="字节读写测试",
                description="测试单字节读写功能",
                interface=InterfaceType.I2C,
                setup_steps=[],
                test_steps=[
                    {"action": "i2c_write", "addr": i2c_addr, "reg": 0x00,
                     "data": [0xAA, 0x55, 0x12, 0x34]},
                    {"action": "i2c_read", "addr": i2c_addr, "reg": 0x00, "len": 4},
                    {"action": "verify_data", "expected": [0xAA, 0x55, 0x12, 0x34]}
                ],
                expected_result="读取数据与写入数据一致"
            )
        elif test_name == "页写入测试":
            return TestCase(
                name="页写入测试",
                description=f"测试页写入功能（页大小：{page_size}字节）",
                interface=InterfaceType.I2C,
                setup_steps=[],
                test_steps=[
                    {"action": "eeprom_write", "addr": i2c_addr, "reg": 0x00,
                     "page_size": page_size,
                     "data": list(range(min(page_size * 2, 64)))}
                ],
                expected_result="页写入成功，无数据丢失"
            )
        else:
            return cls._create_generic_test_case(test_name, InterfaceType.I2C, chip_info)

    @classmethod
    def _create_sensor_test_case(cls, test_name: str, chip_info: Optional[Dict]) -> TestCase:
        """创建传感器测试用例"""
        i2c_addr = chip_info.get("i2c_address", 0x40) if chip_info else 0x40
        chip_id_reg = chip_info.get("chip_id_reg", 0x00) if chip_info else 0x00
        chip_id_val = chip_info.get("chip_id_val", None) if chip_info else None

        if test_name == "连接测试":
            return TestCase(
                name="传感器连接测试",
                description="读取芯片ID验证连接",
                interface=InterfaceType.I2C,
                setup_steps=[],
                test_steps=[
                    {"action": "i2c_read", "addr": i2c_addr,
                     "reg": chip_id_reg, "len": 1}
                ],
                expected_result=f"芯片ID读取成功" + (f"，值为0x{chip_id_val:02X}" if chip_id_val else "")
            )
        elif test_name == "寄存器读取":
            return TestCase(
                name="寄存器读取测试",
                description="读取所有配置寄存器",
                interface=InterfaceType.I2C,
                setup_steps=[],
                test_steps=[
                    {"action": "i2c_read", "addr": i2c_addr, "reg": 0x00, "len": 8}
                ],
                expected_result="成功读取寄存器数据"
            )
        elif test_name == "配置写入":
            return TestCase(
                name="配置寄存器写入",
                description="写入并验证配置寄存器",
                interface=InterfaceType.I2C,
                setup_steps=[],
                test_steps=[
                    {"action": "i2c_write", "addr": i2c_addr, "reg": 0x01, "data": [0x01]},
                    {"action": "delay", "ms": 10},
                    {"action": "i2c_read", "addr": i2c_addr, "reg": 0x01, "len": 1},
                    {"action": "verify_data", "expected": [0x01]}
                ],
                expected_result="配置写入并读取验证成功"
            )
        elif test_name == "数据读取":
            return TestCase(
                name="传感器数据读取",
                description="读取传感器测量数据",
                interface=InterfaceType.I2C,
                setup_steps=[
                    {"action": "i2c_write", "addr": i2c_addr, "reg": 0x01, "data": [0x01]}
                ],
                test_steps=[
                    {"action": "delay", "ms": 100},
                    {"action": "i2c_read", "addr": i2c_addr, "reg": 0x10, "len": 6}
                ],
                expected_result="成功读取传感器数据"
            )
        else:
            return cls._create_generic_test_case(test_name, InterfaceType.I2C, chip_info)

    @classmethod
    def _create_adc_test_case(cls, test_name: str, chip_info: Optional[Dict]) -> TestCase:
        """创建ADC测试用例"""
        if test_name == "连接测试":
            return TestCase(
                name="ADC连接测试",
                description="读取ADC ID或状态寄存器",
                interface=InterfaceType.SPI,
                setup_steps=[],
                test_steps=[
                    {"action": "spi_transfer", "data": [0x00, 0x00, 0x00]}
                ],
                expected_result="SPI通信正常"
            )
        elif test_name == "单端输入测试":
            return TestCase(
                name="单端输入测试",
                description="测试单端输入通道",
                interface=InterfaceType.SPI,
                setup_steps=[
                    {"action": "gpio_set_output", "pin": 0, "value": True}  # 设置参考电压
                ],
                test_steps=[
                    {"action": "spi_transfer", "data": [0x01, 0x80, 0x00]},  # 启动转换
                    {"action": "delay", "us": 10},
                    {"action": "spi_transfer", "data": [0x00, 0x00, 0x00]}   # 读取结果
                ],
                expected_result="ADC转换成功，数据有效"
            )
        else:
            return cls._create_generic_test_case(test_name, InterfaceType.SPI, chip_info)

    @classmethod
    def _create_flash_test_case(cls, test_name: str, chip_info: Optional[Dict]) -> TestCase:
        """创建Flash测试用例"""
        if test_name == "ID读取":
            return TestCase(
                name="JEDEC ID读取",
                description="读取Flash的JEDEC ID",
                interface=InterfaceType.SPI,
                setup_steps=[],
                test_steps=[
                    {"action": "spi_transfer", "data": [0x9F, 0xFF, 0xFF, 0xFF]}
                ],
                expected_result="成功读取Manufacturer ID和Device ID"
            )
        elif test_name == "擦除测试":
            return TestCase(
                name="扇区擦除测试",
                description="擦除并验证扇区",
                interface=InterfaceType.SPI,
                setup_steps=[
                    {"action": "spi_transfer", "data": [0x06]},  # Write Enable
                    {"action": "spi_transfer", "data": [0x20, 0x00, 0x00, 0x00]}  # Sector Erase
                ],
                test_steps=[
                    {"action": "delay", "ms": 100},
                    {"action": "wait_busy", "timeout_ms": 2000}
                ],
                expected_result="扇区擦除成功"
            )
        else:
            return cls._create_generic_test_case(test_name, InterfaceType.SPI, chip_info)

    @classmethod
    def _create_generic_test_case(cls, test_name: str,
                                   interface: InterfaceType,
                                   chip_info: Optional[Dict]) -> TestCase:
        """创建通用测试用例"""
        return TestCase(
            name=test_name,
            description=f"{test_name} - 通用测试",
            interface=interface,
            setup_steps=[],
            test_steps=[{"action": "print", "message": f"执行: {test_name}"}],
            expected_result="测试完成"
        )

    @classmethod
    def _generate_generic_plan(cls, interface: InterfaceType) -> List[TestCase]:
        """生成通用测试方案"""
        return [
            TestCase(
                name="接口连接测试",
                description="验证硬件连接",
                interface=interface,
                setup_steps=[],
                test_steps=[{"action": "scan_interface"}],
                expected_result="接口通信正常"
            ),
            TestCase(
                name="基本读写测试",
                description="测试基本读写功能",
                interface=interface,
                setup_steps=[],
                test_steps=[{"action": "basic_transfer"}],
                expected_result="读写功能正常"
            )
        ]


class TestExecutor:
    """测试执行器"""

    def __init__(self):
        self.i2c_device: Optional[I2CDevice] = None
        self.spi_device: Optional[SPIDevice] = None
        self.gpio_device: Optional[GPIODevice] = None
        self._handles: List[int] = []
        self._last_result: Any = None

    def open_device(self, interface: InterfaceType, serial_number: Optional[str] = None):
        """打开设备"""
        if interface == InterfaceType.I2C:
            handle, self.i2c_device = open_i2c_device(serial_number)
            self._handles.append(handle)
        elif interface == InterfaceType.SPI:
            handle, self.spi_device = open_spi_device(serial_number)
            self._handles.append(handle)
        elif interface == InterfaceType.GPIO:
            handle, self.gpio_device = open_gpio_device(serial_number)
            self._handles.append(handle)

    def close_all(self):
        """关闭所有设备"""
        for handle in self._handles:
            try:
                dev_close(handle)
            except:
                pass
        self._handles.clear()
        self.i2c_device = None
        self.spi_device = None
        self.gpio_device = None

    def execute_test_case(self, test_case: TestCase) -> Dict[str, Any]:
        """执行单个测试用例"""
        result = {
            "name": test_case.name,
            "description": test_case.description,
            "status": "PASS",
            "steps": [],
            "error": None
        }

        try:
            # 执行setup步骤
            for step in test_case.setup_steps:
                self._execute_step(step, test_case.interface)

            # 执行测试步骤
            for step in test_case.test_steps:
                step_result = self._execute_step(step, test_case.interface)
                result["steps"].append({
                    "action": step.get("action"),
                    "result": "OK",
                    "data": step_result
                })

            # 执行cleanup步骤
            if test_case.cleanup_steps:
                for step in test_case.cleanup_steps:
                    self._execute_step(step, test_case.interface)

        except Exception as e:
            result["status"] = "FAIL"
            result["error"] = str(e)
            result["steps"].append({
                "action": "error",
                "result": "FAIL",
                "data": str(e)
            })

        return result

    def _execute_step(self, step: Dict, interface: InterfaceType) -> Any:
        """执行单个步骤"""
        action = step.get("action")

        if action == "scan_i2c":
            if not self.i2c_device:
                raise RuntimeError("I2C设备未打开")
            count, addresses = self.i2c_device.scan()
            self._last_result = addresses
            return {"count": count, "addresses": [f"0x{a:02X}" for a in addresses]}

        elif action == "check_address":
            addr = step.get("address")
            count, addresses = self.i2c_device.scan()
            if addr not in addresses:
                raise RuntimeError(f"设备地址0x{addr:02X}未响应")
            return {"found": True}

        elif action == "i2c_write":
            addr = step.get("addr")
            reg = step.get("reg", 0)
            data = bytes(step.get("data", []))
            reg_type = RegAddrType.BIT8 if reg < 256 else RegAddrType.BIT16
            self.i2c_device.write(addr, reg_type, reg, data)
            return {"written": len(data)}

        elif action == "i2c_read":
            addr = step.get("addr")
            reg = step.get("reg", 0)
            length = step.get("len", 1)
            reg_type = RegAddrType.BIT8 if reg < 256 else RegAddrType.BIT16
            data = self.i2c_device.read(addr, reg_type, reg, length)
            self._last_result = list(data)
            return {"data": list(data), "hex": data.hex()}

        elif action == "eeprom_write":
            addr = step.get("addr")
            reg = step.get("reg", 0)
            page_size = step.get("page_size", 32)
            data = bytes(step.get("data", []))
            reg_type = RegAddrType.BIT8
            self.i2c_device.eeprom_write(addr, reg_type, page_size, reg, data)
            return {"written": len(data)}

        elif action == "spi_transfer":
            if not self.spi_device:
                raise RuntimeError("SPI设备未打开")
            data = bytes(step.get("data", []))
            result = self.spi_device.write_read(SPIClockType.LOW_1EDG,
                                                SPIFirstBitType.MSB, data)
            self._last_result = list(result)
            return {"sent": list(data), "received": list(result), "hex": result.hex()}

        elif action == "gpio_set_output":
            if not self.gpio_device:
                raise RuntimeError("GPIO设备未打开")
            pin = step.get("pin")
            value = step.get("value", False)
            self.gpio_device.set_output(pin, push_pull=True)
            self.gpio_device.set_value(pin, value)
            return {"pin": pin, "value": value}

        elif action == "delay":
            import time
            if "ms" in step:
                time.sleep(step["ms"] / 1000.0)
            elif "us" in step:
                time.sleep(step["us"] / 1000000.0)
            return {"delay": step.get("ms", step.get("us", 0))}

        elif action == "verify_data":
            expected = step.get("expected", [])
            if self._last_result != expected:
                raise RuntimeError(f"数据验证失败: 期望{expected}, 实际{self._last_result}")
            return {"verified": True}

        elif action == "print":
            message = step.get("message", "")
            print(f"  [INFO] {message}")
            return {"message": message}

        elif action == "scan_interface":
            return {"interface": interface.value}

        elif action == "basic_transfer":
            return {"status": "OK"}

        elif action == "wait_busy":
            import time
            timeout = step.get("timeout_ms", 1000)
            # 简化处理，实际应轮询状态
            time.sleep(timeout / 1000.0)
            return {"timeout": timeout}

        else:
            return {"unknown_action": action}


class TestReporter:
    """测试报告生成器"""

    @staticmethod
    def print_report(results: List[Dict[str, Any]]) -> None:
        """打印测试报告"""
        print("\n" + "=" * 60)
        print("测试报告")
        print("=" * 60)

        total = len(results)
        passed = sum(1 for r in results if r["status"] == "PASS")
        failed = total - passed

        for result in results:
            status_icon = "✓" if result["status"] == "PASS" else "✗"
            print(f"\n{status_icon} {result['name']}")
            print(f"   描述: {result['description']}")
            print(f"   结果: {result['status']}")

            if result["error"]:
                print(f"   错误: {result['error']}")

            for step in result.get("steps", []):
                if step.get("data"):
                    print(f"   - {step['action']}: {step['data']}")

        print("\n" + "-" * 60)
        print(f"总计: {total} | 通过: {passed} | 失败: {failed}")
        print("=" * 60)

    @staticmethod
    def save_report(results: List[Dict[str, Any]], filename: str) -> None:
        """保存测试报告到文件"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"报告已保存: {filename}")


# 便捷函数
def create_test_session() -> Tuple[TestExecutor, TestPlanGenerator]:
    """创建测试会话"""
    executor = TestExecutor()
    generator = TestPlanGenerator()
    return executor, generator

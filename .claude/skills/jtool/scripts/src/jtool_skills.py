#!/usr/bin/env python3
"""
JTool Skills - 硬件测试交互式工具

根据需求.md实现：
1. 主动询问用户想测试什么模块
2. 指导用户放置手册到datasheet目录
3. 根据手册询问测试哪方面功能
4. 生成测试方案并执行测试

使用方法:
    python jtool_skills.py
"""

import os
import sys
from pathlib import Path
from typing import Optional, List, Dict, Any

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from jtool import (
    JToolError, DevType, devices_scan, dev_open, dev_close,
    open_i2c_device, open_spi_device, open_gpio_device,
    I2CDevice, SPIDevice, GPIODevice
)
from test_framework import (
    TestExecutor, TestPlanGenerator, TestReporter,
    DatasheetManager, ChipProfile, InterfaceType
)


class Colors:
    """终端颜色"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


class JToolSkills:
    """JTool交互式测试工具"""

    def __init__(self):
        self.datasheet_manager = DatasheetManager()
        self.test_executor = TestExecutor()
        self.current_profile: Optional[ChipProfile] = None
        self.chip_info: Dict[str, Any] = {}

    def print_header(self, text: str) -> None:
        """打印标题"""
        print(f"\n{Colors.HEADER}{'=' * 60}{Colors.ENDC}")
        print(f"{Colors.BOLD}{text}{Colors.ENDC}")
        print(f"{Colors.HEADER}{'=' * 60}{Colors.ENDC}")

    def print_info(self, text: str) -> None:
        """打印信息"""
        print(f"{Colors.BLUE}[INFO]{Colors.ENDC} {text}")

    def print_success(self, text: str) -> None:
        """打印成功信息"""
        print(f"{Colors.GREEN}[OK]{Colors.ENDC} {text}")

    def print_warning(self, text: str) -> None:
        """打印警告"""
        print(f"{Colors.YELLOW}[WARN]{Colors.ENDC} {text}")

    def print_error(self, text: str) -> None:
        """打印错误"""
        print(f"{Colors.RED}[ERROR]{Colors.ENDC} {text}")

    def get_input(self, prompt: str) -> str:
        """获取用户输入"""
        try:
            return input(f"{Colors.CYAN}{prompt}{Colors.ENDC}")
        except KeyboardInterrupt:
            print("\n\n用户取消操作，退出...")
            sys.exit(0)

    def get_choice(self, prompt: str, options: List[str], allow_other: bool = False) -> str:
        """获取用户选择"""
        print(f"\n{Colors.BOLD}{prompt}{Colors.ENDC}")
        for i, opt in enumerate(options, 1):
            print(f"  {i}. {opt}")
        if allow_other:
            print(f"  0. 其他 (手动输入)")

        while True:
            try:
                choice = self.get_input("请选择 (输入数字): ").strip()
                idx = int(choice)
                if allow_other and idx == 0:
                    return self.get_input("请输入: ").strip()
                if 1 <= idx <= len(options):
                    return options[idx - 1]
                self.print_error("无效选择，请重试")
            except ValueError:
                self.print_error("请输入数字")

    def check_datasheets(self) -> bool:
        """检查数据手册目录"""
        datasheets = self.datasheet_manager.list_datasheets()
        if datasheets:
            self.print_success(f"发现 {len(datasheets)} 个数据手册:")
            for ds in datasheets:
                print(f"  - {ds.name}")
            return True
        return False

    def step1_ask_module(self) -> str:
        """步骤1: 询问要测试的模块"""
        self.print_header("步骤1: 选择测试模块")

        # 常见模块类型
        common_modules = [
            "EEPROM (AT24Cxx系列等)",
            "传感器 (温度/湿度/压力等)",
            "ADC (模数转换器)",
            "DAC (数模转换器)",
            "Flash存储器 (SPI Flash)",
            "GPIO扩展器",
            "RTC实时时钟",
            "其他"
        ]

        module_type = self.get_choice(
            "请选择要测试的模块类型:",
            common_modules
        )

        # 获取具体型号
        chip_model = self.get_input(
            f"请输入具体的芯片型号 (例如: AT24C02, BMP280等): "
        ).strip()

        self.chip_info["module_type"] = module_type
        self.chip_info["chip_model"] = chip_model

        return module_type

    def step2_check_datasheet(self) -> Optional[str]:
        """步骤2: 检查数据手册"""
        self.print_header("步骤2: 数据手册检查")

        # 获取主要datasheet目录（项目根目录）
        primary_dir = self.datasheet_manager.get_primary_datasheet_dir()

        # 检查已有数据手册
        if self.check_datasheets():
            use_existing = self.get_input(
                "是否使用现有数据手册? (y/n): "
            ).strip().lower()
            if use_existing == 'y':
                datasheets = self.datasheet_manager.list_datasheets()
                if len(datasheets) == 1:
                    return str(datasheets[0])
                else:
                    ds_name = self.get_choice(
                        "请选择数据手册:",
                        [d.name for d in datasheets]
                    )
                    # 查找选中的文件路径
                    for ds in datasheets:
                        if ds.name == ds_name:
                            return str(ds)
                    return str(datasheets[0])

        # 提示用户放置手册
        self.print_warning("未找到数据手册或选择不使用")
        self.print_info(f"请将数据手册放置到以下目录:")
        print(f"  {primary_dir}")
        print(f"\n支持的格式: PDF, TXT, 图片等")

        # 创建目录
        primary_dir.mkdir(parents=True, exist_ok=True)

        # 询问是否已放置
        while True:
            placed = self.get_input(
                "数据手册已放置后请输入 'done', 或输入 'skip' 跳过: "
            ).strip().lower()

            if placed == 'skip':
                return None
            elif placed == 'done':
                if self.check_datasheets():
                    datasheets = self.datasheet_manager.list_datasheets()
                    if len(datasheets) == 1:
                        return str(datasheets[0])
                    else:
                        ds_name = self.get_choice(
                            "请选择数据手册:",
                            [d.name for d in datasheets]
                        )
                        for ds in datasheets:
                            if ds.name == ds_name:
                                return str(ds)
                        return str(datasheets[0])
                else:
                    self.print_error("仍未找到数据手册，请检查")
            else:
                self.print_error("无效输入，请输入 'done' 或 'skip'")

    def step3_ask_interface(self) -> InterfaceType:
        """步骤3: 询问接口类型"""
        self.print_header("步骤3: 选择通信接口")

        # 根据模块类型推荐接口
        module_type = self.chip_info.get("module_type", "")

        if "EEPROM" in module_type or "传感器" in module_type or "RTC" in module_type:
            self.print_info("根据模块类型，推荐使用 I2C 接口")
            default = "I2C"
        elif "Flash" in module_type or "ADC" in module_type or "DAC" in module_type:
            self.print_info("根据模块类型，推荐使用 SPI 接口")
            default = "SPI"
        else:
            default = "I2C"

        interfaces = ["I2C", "SPI", "GPIO", "CAN"]
        interface_str = self.get_choice(
            f"请选择通信接口 (推荐: {default}):",
            interfaces
        )

        return InterfaceType(interface_str)

    def step4_ask_test_function(self, interface: InterfaceType) -> List[str]:
        """步骤4: 询问测试功能"""
        self.print_header("步骤4: 选择测试功能")

        # 获取芯片类型
        module_type = self.chip_info.get("module_type", "")

        # 映射到模板类型
        chip_type_map = {
            "EEPROM": "eeprom",
            "传感器": "sensor",
            "ADC": "adc",
            "DAC": "dac",
            "Flash": "flash",
            "GPIO": "gpio_expander",
            "RTC": "sensor"
        }

        chip_type = None
        for key, val in chip_type_map.items():
            if key in module_type:
                chip_type = val
                break

        if not chip_type:
            chip_type = "generic"

        # 获取可用测试项
        template = TestPlanGenerator.CHIP_TEMPLATES.get(chip_type, {})
        available_tests = template.get("test_cases", [
            "连接测试",
            "基本读写测试"
        ])

        self.print_info("可选测试项目:")
        for i, test in enumerate(available_tests, 1):
            print(f"  {i}. {test}")

        # 选择测试项
        selection = self.get_input(
            "请输入要执行的测试编号 (多选用逗号分隔, 输入 'all' 执行全部): "
        ).strip()

        if selection.lower() == 'all':
            return available_tests

        try:
            indices = [int(x.strip()) - 1 for x in selection.split(',')]
            selected_tests = []
            for idx in indices:
                if 0 <= idx < len(available_tests):
                    selected_tests.append(available_tests[idx])
            return selected_tests if selected_tests else available_tests
        except ValueError:
            self.print_warning("输入格式错误，将执行全部测试")
            return available_tests

    def step5_configure_device(self, interface: InterfaceType) -> None:
        """步骤5: 配置设备参数"""
        self.print_header("步骤5: 设备参数配置")

        if interface == InterfaceType.I2C:
            addr_input = self.get_input(
                "请输入I2C设备地址 (十六进制, 例如 0x50, 或直接回车自动扫描): "
            ).strip()
            if addr_input:
                try:
                    addr = int(addr_input, 16) if addr_input.startswith('0x') else int(addr_input)
                    self.chip_info["i2c_address"] = addr
                    self.print_success(f"I2C地址设置为: 0x{addr:02X}")
                except ValueError:
                    self.print_warning("地址格式错误，将使用自动扫描")
            else:
                self.print_info("将使用自动扫描检测设备地址")

            # 如果是EEPROM，询问页大小
            if "EEPROM" in self.chip_info.get("module_type", ""):
                page_size = self.get_input(
                    "请输入EEPROM页大小 (字节, 默认32): "
                ).strip()
                self.chip_info["page_size"] = int(page_size) if page_size.isdigit() else 32

        elif interface == InterfaceType.SPI:
            self.print_info("SPI配置:")
            mode = self.get_choice(
                "选择SPI模式:",
                ["模式0 (CPOL=0, CPHA=0)",
                 "模式1 (CPOL=0, CPHA=1)",
                 "模式2 (CPOL=1, CPHA=0)",
                 "模式3 (CPOL=1, CPHA=1)"]
            )
            self.chip_info["spi_mode"] = int(mode[2])  # 提取模式数字

            freq = self.get_input(
                "请输入SPI时钟频率 (KHz, 默认1000): "
            ).strip()
            self.chip_info["spi_freq"] = int(freq) if freq.isdigit() else 1000

    def step6_generate_and_execute(self, interface: InterfaceType,
                                    test_functions: List[str]) -> None:
        """步骤6: 生成测试方案并执行"""
        self.print_header("步骤6: 生成测试方案")

        # 生成测试计划
        module_type = self.chip_info.get("module_type", "")
        chip_type_map = {
            "EEPROM": "eeprom", "传感器": "sensor", "ADC": "adc",
            "DAC": "dac", "Flash": "flash", "GPIO": "gpio_expander"
        }
        chip_type = None
        for key, val in chip_type_map.items():
            if key in module_type:
                chip_type = val
                break

        if not chip_type:
            chip_type = "generic"

        self.print_info("正在生成测试方案...")
        test_cases = TestPlanGenerator.generate_test_plan(
            chip_type, interface, self.chip_info
        )

        # 过滤选中的测试
        if test_functions:
            test_cases = [tc for tc in test_cases if tc.name in test_functions]

        if not test_cases:
            self.print_warning("没有匹配的测试用例，将使用通用测试")
            test_cases = TestPlanGenerator.generate_test_plan(
                "generic", interface, self.chip_info
            )

        # 显示测试计划
        print(f"\n{Colors.BOLD}测试计划:{Colors.ENDC}")
        for i, tc in enumerate(test_cases, 1):
            print(f"  {i}. {tc.name} - {tc.description}")

        # 确认执行
        confirm = self.get_input("\n是否执行测试? (y/n): ").strip().lower()
        if confirm != 'y':
            self.print_info("测试已取消")
            return

        # 打开设备并执行测试
        self.print_header("开始执行测试")

        try:
            # 扫描设备
            self.print_info("扫描JTool设备...")
            devices = devices_scan(DevType[interface.value])
            if not devices:
                self.print_error(f"未找到 {interface.value} 设备")
                return

            self.print_success(f"找到设备: {devices[0]}")

            # 打开设备
            self.print_info("打开设备...")
            self.test_executor.open_device(interface)
            self.print_success("设备已打开")

            # 执行测试
            results = []
            for tc in test_cases:
                print(f"\n{Colors.CYAN}▶ 执行: {tc.name}{Colors.ENDC}")
                result = self.test_executor.execute_test_case(tc)
                results.append(result)

                status_color = Colors.GREEN if result["status"] == "PASS" else Colors.RED
                print(f"  {status_color}结果: {result['status']}{Colors.ENDC}")

                if result["error"]:
                    print(f"  {Colors.RED}错误: {result['error']}{Colors.ENDC}")

            # 打印报告
            TestReporter.print_report(results)

            # 保存报告
            save = self.get_input("\n是否保存测试报告? (y/n): ").strip().lower()
            if save == 'y':
                report_file = f"test_report_{self.chip_info.get('chip_model', 'unknown')}.json"
                TestReporter.save_report(results, report_file)

        except JToolError as e:
            self.print_error(f"JTool错误: {e.message} (代码: {e.code})")
        except Exception as e:
            self.print_error(f"执行错误: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.test_executor.close_all()
            self.print_info("设备已关闭")

    def run(self) -> None:
        """运行交互式测试流程"""
        self.print_header("JTool Skills - 硬件测试工具")

        try:
            # 步骤1: 询问模块
            module_type = self.step1_ask_module()

            # 步骤2: 检查数据手册
            datasheet_path = self.step2_check_datasheet()
            self.chip_info["datasheet_path"] = datasheet_path

            # 步骤3: 选择接口
            interface = self.step3_ask_interface()

            # 步骤4: 选择测试功能
            test_functions = self.step4_ask_test_function(interface)

            # 步骤5: 配置设备
            self.step5_configure_device(interface)

            # 步骤6: 生成方案并执行
            self.step6_generate_and_execute(interface, test_functions)

        except KeyboardInterrupt:
            print(f"\n\n{Colors.YELLOW}用户取消操作{Colors.ENDC}")
        except Exception as e:
            self.print_error(f"发生错误: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.test_executor.close_all()

        self.print_header("测试流程结束")


def quick_test_i2c():
    """快速I2C测试模式"""
    print(f"{Colors.HEADER}快速I2C测试模式{Colors.ENDC}\n")

    executor = TestExecutor()

    try:
        print("扫描I2C设备...")
        devices = devices_scan(DevType.I2C)
        if not devices:
            print("未找到I2C设备")
            return

        print(f"找到设备: {devices[0]}")
        print("打开设备...")
        executor.open_device(InterfaceType.I2C)
        print("扫描I2C总线...")

        count, addresses = executor.i2c_device.scan()
        print(f"\n发现 {count} 个设备:")
        for addr in addresses:
            print(f"  地址: 0x{addr:02X}")

        if addresses:
            addr = addresses[0]
            print(f"\n测试读取设备 0x{addr:02X}...")
            try:
                data = executor.i2c_device.read(addr, RegAddrType.BIT8, 0x00, 4)
                print(f"读取数据: {data.hex()}")
            except Exception as e:
                print(f"读取失败: {e}")

    except Exception as e:
        print(f"错误: {e}")
    finally:
        executor.close_all()


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description='JTool Skills - 硬件测试工具')
    parser.add_argument('--quick', '-q', action='store_true',
                        help='快速测试模式')
    parser.add_argument('--scan', '-s', action='store_true',
                        help='仅扫描设备')

    args = parser.parse_args()

    if args.scan:
        print("扫描所有JTool设备...")
        for dev_type in [DevType.I2C, DevType.SPI, DevType.IO]:
            devices = devices_scan(dev_type)
            print(f"\n{dev_type.name} 设备:")
            if devices:
                for d in devices:
                    print(f"  - {d}")
            else:
                print("  无")
    elif args.quick:
        quick_test_i2c()
    else:
        skills = JToolSkills()
        skills.run()


if __name__ == "__main__":
    main()

"""
芯片测试主模块
整合 datasheet 解析、测试方案生成和测试执行
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any

# 添加脚本目录到路径
script_dir = Path(__file__).parent
if str(script_dir) not in sys.path:
    sys.path.insert(0, str(script_dir))

try:
    from datasheet_parser import DatasheetParser
    from jtool_api import JToolAPI, DevType
    from test_executor import TestExecutor
    from path_resolver import check_environment, get_project_root
except ImportError:
    from .datasheet_parser import DatasheetParser
    from .jtool_api import JToolAPI, DevType
    from .test_executor import TestExecutor
    from .path_resolver import check_environment, get_project_root


class ChipTester:
    """芯片测试主类"""

    def __init__(self):
        """初始化芯片测试器"""
        self.parser = DatasheetParser()
        self.api = JToolAPI()
        self.executor = TestExecutor(self.api)
        self.current_chip = None
        self.chip_info = None

    def check_environment(self) -> Dict[str, Any]:
        """
        检查测试环境

        Returns:
            环境状态字典
        """
        # 使用新的路径解析器检查环境
        env_status = check_environment()

        status = {
            'ready': env_status['ready'],
            'datasheet_ok': env_status['datasheet_exists'] and len(env_status['datasheet_files']) > 0,
            'jtool_ok': env_status['jtool_found'],
            'jtool_path': env_status.get('jtool_path'),
            'datasheet_files': [str(f) for f in env_status['datasheet_files']],
            'messages': env_status['messages'],
            'output_dir_ready': env_status['output_dir_ready'],
        }

        # 尝试扫描设备
        if env_status['jtool_found']:
            try:
                count, devices = self.api.scan_devices()
                status['device_count'] = count
                status['devices'] = devices
            except Exception as e:
                status['device_scan_error'] = str(e)

        return status

        if status['datasheet_ok'] and status['jtool_ok']:
            status['message'] = f'✅ 环境检查通过！找到 {len(ds_status["files"])} 个 datasheet，检测到 {count} 个 jtool 设备'

        return status

    def find_and_parse_datasheet(self, chip_name: str) -> Optional[Dict[str, Any]]:
        """
        查找并解析芯片 datasheet

        Args:
            chip_name: 芯片型号

        Returns:
            芯片信息字典，未找到返回 None
        """
        # 查找 datasheet
        ds_file = self.parser.find_datasheet(chip_name)

        if not ds_file:
            return None

        # 解析文档
        self.chip_info = self.parser.parse_file(ds_file)
        self.current_chip = chip_name

        return self.chip_info

    def generate_test_plans(self) -> List[Dict[str, Any]]:
        """
        根据芯片信息生成测试方案

        Returns:
            测试方案列表
        """
        if not self.chip_info:
            return []

        plans = []
        interfaces = self.chip_info.get('interface', [])
        chip_name = self.chip_info.get('chip_name', 'Unknown')

        # 根据接口类型生成测试方案
        if 'I2C' in interfaces:
            # I2C 连接扫描
            plans.append({
                'id': 'i2c_scan',
                'name': 'I2C 设备扫描',
                'description': '扫描 I2C 总线上的设备，确认芯片是否响应',
                'type': 'i2c_scan',
                'params': {},
            })

            # 获取 I2C 地址
            addresses = self.chip_info.get('i2c_address', [])
            if addresses:
                addr = addresses[0]  # 使用第一个地址

                # 连接测试
                plans.append({
                    'id': 'connection',
                    'name': '设备连接测试',
                    'description': f'验证设备在地址 {addr} 是否响应',
                    'type': 'connection',
                    'params': {'target_addr': addr},
                })

                # 寄存器读取测试
                registers = self.chip_info.get('registers', [])
                if registers:
                    plans.append({
                        'id': 'register_read',
                        'name': '寄存器读取测试',
                        'description': f'读取芯片寄存器值',
                        'type': 'register_read',
                        'params': {
                            'slave_addr': addr.replace('0x', ''),
                            'registers': registers[:5],  # 最多5个寄存器
                        },
                    })

                # EEPROM 专用测试
                if 'eeprom' in chip_name.lower() or any('Kbit' in f for f in self.chip_info.get('features', [])):
                    # 提取页大小
                    page_size = 8  # 默认值
                    for feat in self.chip_info.get('features', []):
                        if 'page' in feat.lower():
                            import re
                            match = re.search(r'(\d+)', feat)
                            if match:
                                page_size = int(match.group(1))

                    plans.append({
                        'id': 'eeprom_write_read',
                        'name': 'EEPROM 写读测试',
                        'description': f'写入数据并读取验证，页大小 {page_size} bytes',
                        'type': 'eeprom_write_read',
                        'params': {
                            'slave_addr': addr.replace('0x', ''),
                            'reg_addr': '00',
                            'page_size': page_size,
                            'chip_type': 'EEPROM',
                        },
                    })

                # 通用写读测试
                plans.append({
                    'id': 'i2c_write_read',
                    'name': 'I2C 写读验证',
                    'description': '写入测试数据并读取验证',
                    'type': 'i2c_write_read',
                    'params': {
                        'slave_addr': addr.replace('0x', ''),
                        'reg_addr': '00',
                        'test_data': ['11', '22', '33', '44'],
                    },
                })

        if 'SPI' in interfaces:
            plans.append({
                'id': 'spi_connection',
                'name': 'SPI 连接测试',
                'description': '测试 SPI 通信连接',
                'type': 'spi_test',
                'params': {},
            })

        return plans

    def run_test(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行单个测试方案

        Args:
            plan: 测试方案

        Returns:
            测试结果
        """
        return self.executor.execute_test(plan['type'], plan['params'])

    def run_all_tests(self, plans: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        执行所有测试方案

        Args:
            plans: 测试方案列表

        Returns:
            测试结果列表
        """
        results = []
        for plan in plans:
            print(f"\n执行测试: {plan['name']}")
            result = self.run_test(plan)
            results.append(result)
            status = "[PASS]" if result.get('success') else "[FAIL]"
            print(f"结果: {status}")
        return results

    def save_results(self, results: List[Dict[str, Any]]) -> Dict[str, str]:
        """
        保存测试结果

        Args:
            results: 测试结果列表

        Returns:
            保存的文件路径
        """
        if not self.current_chip or not self.chip_info:
            return {}

        return self.executor.save_results(
            self.current_chip,
            self.chip_info,
            results
        )

    def get_available_chips(self) -> List[str]:
        """
        获取可用的芯片列表

        Returns:
            芯片名称列表
        """
        files = self.parser.list_all_datasheets()
        # 从文件名提取芯片名
        chips = []
        for f in files:
            name = f.replace('.pdf', '').replace('.docx', '').replace('.doc', '')
            name = name.replace('.md', '').replace('.html', '').replace('.txt', '')
            chips.append(name)
        return chips



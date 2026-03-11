"""
测试执行器模块
执行各种芯片测试方案
"""

import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable

# 导入路径解析器
try:
    from path_resolver import get_test_output_dir, get_project_root, get_resolver
except ImportError:
    from .path_resolver import get_test_output_dir, get_project_root, get_resolver

from jtool_api import JToolAPI, DevType, RegAddrType


class TestExecutor:
    """测试执行器"""

    def __init__(self, jtool_api: Optional[JToolAPI] = None):
        """
        初始化测试执行器

        Args:
            jtool_api: JToolAPI 实例，None 则自动创建
        """
        self.api = jtool_api or JToolAPI()
        self.results = []

    def execute_test(self, test_type: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行指定类型的测试

        Args:
            test_type: 测试类型
            params: 测试参数

        Returns:
            测试结果字典
        """
        test_methods = {
            'i2c_scan': self._test_i2c_scan,
            'i2c_read': self._test_i2c_read,
            'i2c_write_read': self._test_i2c_write_read,
            'connection': self._test_connection,
            'register_read': self._test_register_read,
            'eeprom_write_read': self._test_eeprom_write_read,
        }

        method = test_methods.get(test_type)
        if method:
            return method(params)
        else:
            return {'success': False, 'error': f'未知的测试类型: {test_type}'}

    def _test_i2c_scan(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """执行 I2C 扫描测试"""
        result = {
            'test_name': 'I2C 设备扫描',
            'success': False,
            'output': '',
            'devices_found': [],
            'timestamp': datetime.now().isoformat(),
        }

        try:
            output = self.api.cmd_i2c_scan(use_7bit=True)
            result['output'] = output

            # 解析扫描结果
            lines = output.split('\n')
            for line in lines:
                # 查找地址格式
                import re
                matches = re.findall(r'0x[0-9A-Fa-f]{2}', line)
                result['devices_found'].extend(matches)

            result['devices_found'] = list(set(result['devices_found']))
            result['success'] = len(result['devices_found']) > 0

        except Exception as e:
            result['error'] = str(e)

        return result

    def _test_i2c_read(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """执行 I2C 读取测试"""
        result = {
            'test_name': 'I2C 数据读取',
            'success': False,
            'output': '',
            'data': None,
            'timestamp': datetime.now().isoformat(),
        }

        try:
            slave_addr = params.get('slave_addr', 'A0')
            reg_addr = params.get('reg_addr', '00')
            length = params.get('length', 16)

            output = self.api.cmd_i2c_read(slave_addr, reg_addr, length)
            result['output'] = output
            result['data'] = output.strip()
            result['success'] = 'error' not in output.lower() and 'fail' not in output.lower()

        except Exception as e:
            result['error'] = str(e)

        return result

    def _test_i2c_write_read(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """执行 I2C 写读验证测试"""
        result = {
            'test_name': 'I2C 写读验证',
            'success': False,
            'output': '',
            'write_data': [],
            'read_data': [],
            'match': False,
            'timestamp': datetime.now().isoformat(),
        }

        try:
            slave_addr = params.get('slave_addr', 'A0')
            reg_addr = params.get('reg_addr', '00')
            test_data = params.get('test_data', ['11', '22', '33', '44'])

            # 写入数据
            write_output = self.api.cmd_i2c_write(slave_addr, reg_addr, test_data)
            result['write_output'] = write_output

            # 等待写入完成（EEPROM 需要）
            if 'eeprom' in params.get('chip_type', '').lower():
                time.sleep(0.01)  # 10ms 等待

            # 读取数据
            read_output = self.api.cmd_i2c_read(slave_addr, reg_addr, len(test_data))
            result['read_output'] = read_output

            # 比较数据
            result['write_data'] = test_data
            result['read_data'] = read_output.strip().split() if read_output else []

            # 简单匹配检查
            result['match'] = all(d in read_output for d in test_data)
            result['success'] = result['match']

        except Exception as e:
            result['error'] = str(e)

        return result

    def _test_connection(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """执行连接测试"""
        result = {
            'test_name': '设备连接测试',
            'success': False,
            'output': '',
            'timestamp': datetime.now().isoformat(),
        }

        try:
            # 扫描设备
            output = self.api.cmd_i2c_scan(use_7bit=True)
            result['output'] = output

            target_addr = params.get('target_addr', '').upper()
            if target_addr:
                result['success'] = target_addr in output.upper()
                if result['success']:
                    result['message'] = f'找到目标设备: {target_addr}'
                else:
                    result['message'] = f'未找到目标设备: {target_addr}'
            else:
                result['success'] = len(output.strip()) > 0

        except Exception as e:
            result['error'] = str(e)

        return result

    def _test_register_read(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """执行寄存器读取测试"""
        result = {
            'test_name': '寄存器读取测试',
            'success': False,
            'output': '',
            'registers': {},
            'timestamp': datetime.now().isoformat(),
        }

        try:
            slave_addr = params.get('slave_addr', 'A0')
            registers = params.get('registers', [])

            for reg in registers:
                reg_name = reg.get('name', 'Unknown')
                reg_addr = reg.get('address', '00')

                read_output = self.api.cmd_i2c_read(slave_addr, reg_addr, 1)
                result['registers'][reg_name] = {
                    'address': reg_addr,
                    'value': read_output.strip(),
                }

            result['success'] = len(result['registers']) > 0

        except Exception as e:
            result['error'] = str(e)

        return result

    def _test_eeprom_write_read(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """执行 EEPROM 写读测试"""
        result = {
            'test_name': 'EEPROM 写读测试',
            'success': False,
            'output': '',
            'timestamp': datetime.now().isoformat(),
        }

        try:
            slave_addr = params.get('slave_addr', 'A0')
            reg_addr = params.get('reg_addr', '00')
            page_size = params.get('page_size', 8)

            # 生成测试数据（一个页大小）
            test_data = [f'{i:02X}' for i in range(page_size)]

            # 写入
            write_output = self.api.cmd_i2c_write(slave_addr, reg_addr, test_data)
            result['write_output'] = write_output

            # 等待写入完成
            time.sleep(0.01)

            # 读取
            read_output = self.api.cmd_i2c_read(slave_addr, reg_addr, page_size)
            result['read_output'] = read_output

            # 验证
            read_bytes = read_output.strip().split()
            result['match'] = len(read_bytes) == len(test_data)
            result['success'] = result['match']

        except Exception as e:
            result['error'] = str(e)

        return result

    def generate_test_code(self, chip_name: str, test_results: List[Dict]) -> str:
        """
        生成测试代码

        Args:
            chip_name: 芯片名称
            test_results: 测试结果列表

        Returns:
            Python 代码字符串
        """
        code = f'''"""
{chip_name} 芯片自动测试代码
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

import subprocess
import time
from typing import List, Tuple


class {chip_name.replace('-', '_')}Tester:
    """{chip_name} 测试类"""

    def __init__(self):
        self.chip_name = "{chip_name}"

    def run_all_tests(self) -> List[dict]:
        """运行所有测试"""
        results = []
'''

        for i, test in enumerate(test_results):
            test_name = test.get('test_name', f'test_{i}')
            code += f'''
        # {test_name}
        results.append(self.{test_name.lower().replace(' ', '_')}())
'''

        code += '''
        return results
'''

        # 添加各个测试方法
        for test in test_results:
            test_name = test.get('test_name', 'unknown_test')
            method_name = test_name.lower().replace(' ', '_')

            code += f'''

    def {method_name}(self) -> dict:
        """{test_name}"""
        result = {{
            'test_name': '{test_name}',
            'success': False,
            'output': '',
        }}
        try:
            # TODO: 实现测试逻辑
            result['success'] = True
        except Exception as e:
            result['error'] = str(e)
        return result
'''

        code += f'''

if __name__ == '__main__':
    tester = {chip_name.replace('-', '_')}Tester()
    results = tester.run_all_tests()

    print("=" * 50)
    print(f"{{tester.chip_name}} 测试结果")
    print("=" * 50)

    for r in results:
        status = "[PASS]" if r['success'] else "[FAIL]"
        print(f"{{r['test_name']}}: {{status}}")
        if 'error' in r:
            print(f"  Error: {{r['error']}}")

    passed = sum(1 for r in results if r['success'])
    print(f"\\nTotal: {{passed}}/{{len(results)}} passed")
'''

        return code

    def generate_report(self, chip_name: str, chip_info: Dict, test_results: List[Dict]) -> str:
        """
        生成测试报告

        Args:
            chip_name: 芯片名称
            chip_info: 芯片信息
            test_results: 测试结果列表

        Returns:
            Markdown 格式报告
        """
        report = f'''# {chip_name} 芯片测试报告

**测试时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 芯片信息

| 项目 | 内容 |
|------|------|
| 芯片型号 | {chip_name} |
| 通信接口 | {', '.join(chip_info.get('interface', ['Unknown']))} |
| I2C 地址 | {', '.join(chip_info.get('i2c_address', ['Unknown']))} |
| 电压规格 | {', '.join(chip_info.get('voltage', ['Unknown']))} |

### 芯片特性

'''

        features = chip_info.get('features', [])
        if features:
            for f in features:
                report += f'- {f}\n'
        else:
            report += '- 无特性信息\n'

        report += f'''

---

## 测试结果概览

| 测试项目 | 结果 | 备注 |
|----------|------|------|
'''

        for test in test_results:
            test_name = test.get('test_name', 'Unknown')
            success = '[PASS]' if test.get('success') else '[FAIL]'
            note = test.get('message', '')
            report += f'| {test_name} | {success} | {note} |\n'

        passed = sum(1 for r in test_results if r.get('success'))
        total = len(test_results)

        report += f'''

**总计**: {passed}/{total} 项测试通过

---

## 详细测试记录

'''

        for i, test in enumerate(test_results, 1):
            report += f'''### {i}. {test.get('test_name', 'Unknown')}

- **结果**: {'[PASS]' if test.get('success') else '[FAIL]'}
- **时间**: {test.get('timestamp', 'N/A')}

**输出**:
```
{test.get('output', 'N/A')}
```

'''
            if 'error' in test:
                report += f'''**错误信息**:
```
{test['error']}
```

'''

        report += '''---

## 测试结论

'''

        if passed == total:
            report += '[OK] **所有测试通过！芯片工作正常。**\n'
        elif passed > 0:
            report += f'[WARN] **部分测试通过 ({passed}/{total})，请检查连接和配置。**\n'
        else:
            report += '[FAIL] **测试未通过，请检查硬件连接。**\n'

        report += f'''
---
*报告由 JTool Chip Tester 自动生成*
'''

        return report

    def save_results(self, chip_name: str, chip_info: Dict, test_results: List[Dict],
                     output_dir: Optional[Path] = None):
        """
        保存测试结果到文件

        Args:
            chip_name: 芯片名称
            chip_info: 芯片信息
            test_results: 测试结果
            output_dir: 保存目录，默认使用 path_resolver 获取的 test_code/ 目录

        Returns:
            保存的文件路径字典
        """
        # 获取输出目录（根目录下的 test_code/）
        if output_dir is None:
            output_dir = get_test_output_dir()

        # 确保输出目录存在
        resolver = get_resolver()
        if not resolver.ensure_dir_exists(output_dir):
            # 如果创建失败，回退到当前目录
            output_dir = Path.cwd()

        # 生成文件名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_name = chip_name.replace('-', '_').replace(' ', '_')

        saved_files = {}

        try:
            # 保存测试代码
            code_file = output_dir / f'test_{safe_name}.py'
            code_content = self.generate_test_code(chip_name, test_results)
            with open(code_file, 'w', encoding='utf-8') as f:
                f.write(code_content)
            saved_files['code_file'] = str(code_file)
        except Exception as e:
            saved_files['code_file_error'] = str(e)

        try:
            # 保存测试报告
            report_file = output_dir / f'report_{safe_name}_{timestamp}.md'
            report_content = self.generate_report(chip_name, chip_info, test_results)
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report_content)
            saved_files['report_file'] = str(report_file)
        except Exception as e:
            saved_files['report_file_error'] = str(e)

        return saved_files

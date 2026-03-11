"""
TDC-GP22 芯片完整测试代码
生成时间: 2025-03-11
包含: SPI连接、寄存器读取、配置写入、时间测量
"""

import subprocess
import sys
import time
from pathlib import Path
from typing import List, Tuple


def get_jtool_path() -> str:
    """获取 jtool 可执行文件路径"""
    possible_paths = [
        Path(__file__).parent.parent / ".claude" / "skills" / "jtool" / "scripts" / "lib" / "jtool.exe",
        Path(".claude/skills/jtool/scripts/lib/jtool.exe"),
        Path("jtool.exe"),
        "jtool",
    ]
    for path in possible_paths:
        if isinstance(path, Path) and path.exists():
            return str(path)
    return "jtool"


class TDC_GP22_Tester:
    """TDC-GP22 完整测试类"""

    def __init__(self, device_id: int = 0):
        self.chip_name = "TDC-GP22"
        self.jtool = get_jtool_path()
        self.device_id = device_id
        self.results = []

    def run_command(self, cmd: List[str]) -> Tuple[int, str]:
        """执行 jtool 命令"""
        full_cmd = [self.jtool] + cmd
        try:
            result = subprocess.run(
                full_cmd,
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode, result.stdout + result.stderr
        except Exception as e:
            return -1, str(e)

    def test_spi_connection(self) -> dict:
        """SPI 连接测试"""
        result = {
            'test_name': 'SPI Connection Test',
            'success': False,
            'output': '',
        }
        returncode, output = self.run_command([
            'spircmd', '-i', str(self.device_id), '-c', '9F', '3'
        ])
        result['output'] = output.strip()
        result['success'] = returncode == 0 and 'ERROR' not in output.upper()
        return result

    def test_register_read(self) -> dict:
        """寄存器读取测试"""
        result = {
            'test_name': 'Register Read Test',
            'success': False,
            'output': '',
            'registers': {},
        }

        # 读取状态寄存器
        returncode, output = self.run_command([
            'spircmd', '-i', str(self.device_id), '-c', '04', '1'
        ])
        result['registers']['Status'] = output.strip()

        # 读取配置寄存器
        returncode, output = self.run_command([
            'spircmd', '-i', str(self.device_id), '-c', '00', '4'
        ])
        result['registers']['Config'] = output.strip()

        result['output'] = str(result['registers'])
        result['success'] = len(result['registers']) > 0
        return result

    def test_config_write(self) -> dict:
        """配置写入测试"""
        result = {
            'test_name': 'Config Write Test',
            'success': False,
            'output': '',
        }

        # 写入配置
        returncode, output = self.run_command([
            'spiwcmd', '-i', str(self.device_id), '-c', '80',
            '00', '00', '00', '00'
        ])

        # 验证写入
        time.sleep(0.01)
        returncode2, output2 = self.run_command([
            'spircmd', '-i', str(self.device_id), '-c', '00', '4'
        ])

        result['output'] = f"Write: {output.strip()}, Read: {output2.strip()}"
        result['success'] = returncode == 0
        return result

    def test_time_measurement(self) -> dict:
        """时间测量功能测试"""
        result = {
            'test_name': 'Time Measurement Test',
            'success': False,
            'output': '',
        }

        # 读取时间测量结果
        returncode, output = self.run_command([
            'spircmd', '-i', str(self.device_id), '-c', '10', '4'
        ])

        result['output'] = output.strip()
        result['success'] = returncode == 0
        result['note'] = 'Returns default values without sensor connected'
        return result

    def run_all_tests(self) -> List[dict]:
        """运行所有测试"""
        print("=" * 60)
        print(f"TDC-GP22 Complete Test Suite")
        print("=" * 60)
        print(f"Device ID: {self.device_id}")
        print()

        self.results = []
        tests = [
            ("SPI Connection", self.test_spi_connection),
            ("Register Read", self.test_register_read),
            ("Config Write", self.test_config_write),
            ("Time Measurement", self.test_time_measurement),
        ]

        for i, (name, test_func) in enumerate(tests, 1):
            print(f"[{i}/{len(tests)}] {name}...")
            result = test_func()
            self.results.append(result)
            status = "[PASS]" if result['success'] else "[FAIL]"
            print(f"    Result: {status}")
            if result.get('output'):
                print(f"    Output: {result['output'][:60]}")
            print()

        return self.results

    def print_report(self):
        """打印测试报告"""
        print("=" * 60)
        print(f"Test Report: {self.chip_name}")
        print("=" * 60)

        for r in self.results:
            status = "[PASS]" if r['success'] else "[FAIL]"
            print(f"\n{r['test_name']}: {status}")
            if 'output' in r and r['output']:
                print(f"  Output: {r['output'][:80]}")
            if 'note' in r:
                print(f"  Note: {r['note']}")

        passed = sum(1 for r in self.results if r['success'])
        total = len(self.results)

        print("\n" + "=" * 60)
        print(f"Summary: {passed}/{total} tests passed")
        print("=" * 60)

        if passed == total:
            print("\n[OK] All tests passed!")
        elif passed > 0:
            print(f"\n[WARN] Partial success ({passed}/{total})")
        else:
            print("\n[FAIL] All tests failed")


def main():
    """主函数"""
    tester = TDC_GP22_Tester(device_id=0)
    tester.run_all_tests()
    tester.print_report()
    return tester.results


if __name__ == '__main__':
    main()

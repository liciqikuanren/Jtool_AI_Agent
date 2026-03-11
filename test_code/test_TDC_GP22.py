"""
TDC-GP22 芯片自动测试代码
生成时间: 2025-03-11
"""

import subprocess
import sys
from pathlib import Path
from typing import List, Tuple


def get_jtool_path() -> str:
    """获取 jtool 可执行文件路径"""
    # 尝试多种路径
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
    """TDC-GP22 测试类"""

    def __init__(self):
        self.chip_name = "TDC-GP22"
        self.jtool = get_jtool_path()

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
        """SPI 连接测试 - 发送读取 ID 指令"""
        result = {
            'test_name': 'SPI Connection Test',
            'success': False,
            'output': '',
        }

        # 发送读取 ID 指令 (0x9F) 读取 3 字节
        returncode, output = self.run_command(['spircmd', '-i', '0', '-c', '9F', '3'])

        result['output'] = output.strip()
        result['success'] = returncode == 0 and 'ERROR' not in output.upper()

        return result

    def test_register_read(self) -> dict:
        """寄存器读取测试"""
        result = {
            'test_name': 'Register Read Test',
            'success': False,
            'output': '',
        }

        # 读取状态寄存器
        returncode, output = self.run_command(['spircmd', '-i', '0', '-c', '04', '1'])

        result['output'] = output.strip()
        result['success'] = returncode == 0

        return result

    def test_config_write(self) -> dict:
        """配置写入测试"""
        result = {
            'test_name': 'Config Write Test',
            'success': False,
            'output': '',
        }

        # 写入配置寄存器
        returncode, output = self.run_command(['spiwcmd', '-i', '0', '-c', '80', '00', '00', '00', '00'])

        result['output'] = output.strip()
        result['success'] = returncode == 0

        return result

    def run_all_tests(self) -> List[dict]:
        """运行所有测试"""
        print("=" * 50)
        print(f"Testing {self.chip_name}")
        print("=" * 50)

        results = []

        print("\n[1/3] SPI Connection Test...")
        results.append(self.test_spi_connection())
        print(f"  Result: {'[PASS]' if results[-1]['success'] else '[FAIL]'}")

        print("\n[2/3] Register Read Test...")
        results.append(self.test_register_read())
        print(f"  Result: {'[PASS]' if results[-1]['success'] else '[FAIL]'}")

        print("\n[3/3] Config Write Test...")
        results.append(self.test_config_write())
        print(f"  Result: {'[PASS]' if results[-1]['success'] else '[FAIL]'}")

        return results


def main():
    """主函数"""
    tester = TDC_GP22_Tester()
    results = tester.run_all_tests()

    print("\n" + "=" * 50)
    print(f"{tester.chip_name} Test Report")
    print("=" * 50)

    for r in results:
        status = "[PASS]" if r['success'] else "[FAIL]"
        print(f"\n{r['test_name']}: {status}")
        if r['output']:
            print(f"  Output: {r['output'][:100]}")

    passed = sum(1 for r in results if r['success'])
    total = len(results)

    print("\n" + "=" * 50)
    print(f"Total: {passed}/{total} passed")
    print("=" * 50)

    return results


if __name__ == '__main__':
    main()

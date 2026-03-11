"""
示例测试代码 - 演示 JTool 使用方法
芯片: 示例芯片
生成时间: 2025-03-11
"""

import sys
from pathlib import Path

# 添加技能脚本路径
script_path = Path(__file__).parent.parent / ".claude" / "skills" / "jtool" / "scripts"
if str(script_path) not in sys.path:
    sys.path.insert(0, str(script_path))

from chip_tester import ChipTester


def main():
    """主函数"""
    print("=" * 60)
    print("JTool 芯片测试示例")
    print("=" * 60)

    tester = ChipTester()

    # 检查环境
    print("\n1. 检查环境...")
    status = tester.check_environment()

    for msg in status['messages']:
        print(f"   {msg}")

    if not status['ready']:
        print("\n环境未就绪，请检查:")
        print("- jtool 是否正确安装")
        print("- datasheet 文件夹是否存在并有芯片手册")
        return

    # 列出可用芯片
    print("\n2. 可用芯片:")
    for chip_file in status.get('datasheet_files', []):
        chip_name = Path(chip_file).stem
        print(f"   - {chip_name}")

    print("\n" + "=" * 60)
    print("环境检查通过！可以使用 jtool skill 进行芯片测试。")
    print("=" * 60)


if __name__ == '__main__':
    main()

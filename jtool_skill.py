#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JTool Skill - Claude Code Skill Entry Point

Usage:
    python jtool_skill.py [command] [options]

Commands:
    interactive     启动交互式测试向导 (默认)
    scan            扫描JTool设备
    quick           快速I2C测试
    test-eeprom     测试AT24C02 EEPROM
    test-flash      测试W25Q Flash
    help            显示帮助信息
"""

import sys
import io
import argparse
from pathlib import Path

# 设置UTF-8输出
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 添加src到路径（新位置：.claude/skills/jtool/scripts/src）
sys.path.insert(0, str(Path(__file__).parent / ".claude" / "skills" / "jtool" / "scripts" / "src"))

def main():
    parser = argparse.ArgumentParser(
        prog='jtool',
        description='JTool USB适配器硬件测试框架',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  python jtool_skill.py                    # 交互式模式
  python jtool_skill.py scan               # 扫描设备
  python jtool_skill.py quick              # 快速测试
  python jtool_skill.py test-eeprom        # 测试EEPROM
  python jtool_skill.py test-flash         # 测试Flash
        '''
    )

    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # interactive 命令
    interactive_parser = subparsers.add_parser(
        'interactive',
        help='启动交互式测试向导',
        aliases=['i', 'skill']
    )

    # scan 命令
    scan_parser = subparsers.add_parser(
        'scan',
        help='扫描所有连接的JTool设备'
    )

    # quick 命令
    quick_parser = subparsers.add_parser(
        'quick',
        help='快速I2C测试模式'
    )

    # test-eeprom 命令
    eeprom_parser = subparsers.add_parser(
        'test-eeprom',
        help='测试AT24C02 EEPROM'
    )
    eeprom_parser.add_argument(
        '--addr', '-a',
        type=lambda x: int(x, 16),
        default=0x50,
        help='I2C地址 (十六进制, 默认: 0x50)'
    )

    # test-flash 命令
    flash_parser = subparsers.add_parser(
        'test-flash',
        help='测试W25Q SPI Flash'
    )

    args = parser.parse_args()

    # 如果没有指定命令，默认进入交互式模式
    if not args.command:
        command = 'interactive'
    else:
        command = args.command

    try:
        if command in ('interactive', 'i', 'skill'):
            from jtool_skills import main as skills_main
            skills_main()

        elif command == 'scan':
            from scan_devices import scan_all_devices
            scan_all_devices()

        elif command == 'quick':
            from jtool_skills import quick_test_i2c
            quick_test_i2c()

        elif command == 'test-eeprom':
            from examples.test_eeprom_at24c02 import test_at24c02
            success = test_at24c02(args.addr if hasattr(args, 'addr') else 0x50)
            sys.exit(0 if success else 1)

        elif command == 'test-flash':
            from examples.test_flash_w25q import test_w25q
            success = test_w25q()
            sys.exit(0 if success else 1)

        else:
            parser.print_help()

    except KeyboardInterrupt:
        print("\n\n操作已取消")
        sys.exit(130)
    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

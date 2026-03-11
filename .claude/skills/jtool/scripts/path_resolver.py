"""
路径解析模块 - 自动查找 jtool 和相关资源的路径
提高跨平台、跨目录结构的兼容性
"""

import os
import sys
from pathlib import Path
from typing import Optional, List


class PathResolver:
    """路径解析器 - 自动查找项目中的各种路径"""

    # 可能的 jtool 位置（相对于项目根目录）
    JTOOL_RELATIVE_PATHS = [
        ".claude/skills/jtool/scripts/lib/jtool.exe",
        ".claude/skills/jtool/scripts/lib/jtool",
        "skills/jtool/scripts/lib/jtool.exe",
        "skills/jtool/scripts/lib/jtool",
    ]

    # 可能的 datasheet 位置
    DATASHEET_RELATIVE_PATHS = [
        "datasheet",
        "datasheets",
        "docs/datasheet",
        "docs/datasheets",
    ]

    def __init__(self):
        self._project_root: Optional[Path] = None
        self._jtool_path: Optional[Path] = None
        self._datasheet_dir: Optional[Path] = None

    @property
    def project_root(self) -> Path:
        """
        自动查找项目根目录
        通过查找 .claude 文件夹或 .git 文件夹来确定
        """
        if self._project_root is None:
            self._project_root = self._find_project_root()
        return self._project_root

    def _find_project_root(self) -> Path:
        """
        查找项目根目录
        策略：从当前文件向上查找，直到找到 .claude 或 .git 文件夹
        """
        # 从当前文件开始向上查找
        current = Path(__file__).resolve().parent

        for _ in range(10):  # 最多向上查找10层
            # 检查是否是项目根目录的标志
            if (current / ".claude").exists():
                return current
            if (current / ".git").exists():
                return current
            if (current / "datasheet").exists():
                return current

            parent = current.parent
            if parent == current:  # 到达根目录
                break
            current = parent

        # 如果找不到，返回当前工作目录
        return Path.cwd()

    def get_jtool_path(self) -> Optional[Path]:
        """
        获取 jtool 可执行文件路径
        先查找相对路径，再查找系统 PATH
        """
        if self._jtool_path is None:
            self._jtool_path = self._find_jtool()
        return self._jtool_path

    def _find_jtool(self) -> Optional[Path]:
        """查找 jtool 可执行文件"""
        # 1. 先尝试相对路径
        for rel_path in self.JTOOL_RELATIVE_PATHS:
            full_path = self.project_root / rel_path
            if full_path.exists():
                return full_path

        # 2. 尝试环境变量或系统 PATH
        jtool_cmd = "jtool.exe" if sys.platform == "win32" else "jtool"

        # 检查 PATH 中是否存在
        for path_dir in os.environ.get("PATH", "").split(os.pathsep):
            path_file = Path(path_dir) / jtool_cmd
            if path_file.exists():
                return path_file

        # 3. 尝试直接使用命令（如果在 PATH 中）
        return Path(jtool_cmd)

    def get_datasheet_dir(self) -> Path:
        """
        获取 datasheet 文件夹路径
        如果不存在，返回默认路径
        """
        if self._datasheet_dir is None:
            self._datasheet_dir = self._find_datasheet_dir()
        return self._datasheet_dir

    def _find_datasheet_dir(self) -> Path:
        """查找 datasheet 文件夹"""
        for rel_path in self.DATASHEET_RELATIVE_PATHS:
            full_path = self.project_root / rel_path
            if full_path.exists():
                return full_path

        # 默认返回根目录下的 datasheet
        return self.project_root / "datasheet"

    def get_test_output_dir(self) -> Path:
        """
        获取测试代码输出目录
        返回根目录下的 test_code/ 文件夹
        """
        output_dir = self.project_root / "test_code"
        return output_dir

    def ensure_dir_exists(self, path: Path) -> bool:
        """
        确保目录存在，如果不存在则创建

        Returns:
            True: 目录已存在或创建成功
            False: 创建失败
        """
        try:
            path.mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            print(f"[警告] 无法创建目录 {path}: {e}")
            return False

    def check_environment(self) -> dict:
        """
        检查环境是否就绪

        Returns:
            {
                'ready': bool,           # 是否可以运行测试
                'jtool_found': bool,     # 是否找到 jtool
                'jtool_path': Path,      # jtool 路径
                'datasheet_exists': bool, # datasheet 文件夹是否存在
                'datasheet_files': list,  # datasheet 文件列表
                'output_dir_ready': bool, # 输出目录是否就绪
                'messages': list,         # 状态消息列表
            }
        """
        result = {
            'ready': False,
            'jtool_found': False,
            'jtool_path': None,
            'datasheet_exists': False,
            'datasheet_files': [],
            'output_dir_ready': False,
            'messages': [],
        }

        # 检查 jtool
        jtool_path = self.get_jtool_path()
        if jtool_path and jtool_path.exists():
            result['jtool_found'] = True
            result['jtool_path'] = jtool_path
            result['messages'].append(f"[OK] 找到 jtool: {jtool_path}")
        else:
            result['messages'].append("[错误] 未找到 jtool，请确保 jtool 已安装或在正确位置")
            result['messages'].append(f"      查找路径: {jtool_path}")

        # 检查 datasheet
        ds_dir = self.get_datasheet_dir()
        if ds_dir.exists():
            result['datasheet_exists'] = True
            # 获取支持的文件
            supported_exts = ['.pdf', '.docx', '.doc', '.md', '.html', '.htm', '.txt']
            for ext in supported_exts:
                result['datasheet_files'].extend(ds_dir.glob(f'*{ext}'))

            if result['datasheet_files']:
                result['messages'].append(f"[OK] 找到 {len(result['datasheet_files'])} 个 datasheet 文件")
            else:
                result['messages'].append(f"[警告] datasheet 文件夹为空: {ds_dir}")
        else:
            result['messages'].append(f"[警告] datasheet 文件夹不存在: {ds_dir}")
            result['messages'].append("      请创建文件夹并放入芯片手册")

        # 检查输出目录
        output_dir = self.get_test_output_dir()
        if self.ensure_dir_exists(output_dir):
            result['output_dir_ready'] = True
            result['messages'].append(f"[OK] 输出目录就绪: {output_dir}")
        else:
            result['messages'].append(f"[警告] 输出目录可能不可用: {output_dir}")

        # 判断是否就绪
        result['ready'] = result['jtool_found']

        return result


# 全局实例
_path_resolver = None


def get_resolver() -> PathResolver:
    """获取路径解析器实例"""
    global _path_resolver
    if _path_resolver is None:
        _path_resolver = PathResolver()
    return _path_resolver


# 便捷函数
def get_jtool_path() -> Optional[Path]:
    """获取 jtool 路径"""
    return get_resolver().get_jtool_path()


def get_datasheet_dir() -> Path:
    """获取 datasheet 目录"""
    return get_resolver().get_datasheet_dir()


def get_test_output_dir() -> Path:
    """获取测试输出目录"""
    return get_resolver().get_test_output_dir()


def get_project_root() -> Path:
    """获取项目根目录"""
    return get_resolver().project_root


def check_environment() -> dict:
    """检查环境"""
    return get_resolver().check_environment()

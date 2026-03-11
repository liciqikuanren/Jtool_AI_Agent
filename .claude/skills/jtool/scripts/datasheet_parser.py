"""
Datasheet 文档解析模块
支持 PDF, Word, Markdown, HTML, 文本文件以及扫描件 OCR
"""

import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any

# 导入路径解析器
try:
    from path_resolver import get_datasheet_dir, get_project_root, get_resolver
except ImportError:
    from .path_resolver import get_datasheet_dir, get_project_root, get_resolver


class DatasheetParser:
    """芯片手册解析器"""

    def __init__(self, datasheet_dir: Optional[str] = None):
        """
        初始化解析器

        Args:
            datasheet_dir: datasheet 文件夹路径，None 则自动查找
        """
        if datasheet_dir is None:
            # 使用路径解析器自动查找
            self.datasheet_dir = get_datasheet_dir()
        else:
            self.datasheet_dir = Path(datasheet_dir)

        self.supported_formats = ['.pdf', '.docx', '.doc', '.md', '.html', '.htm', '.txt']

    def check_datasheet_folder(self) -> Dict[str, Any]:
        """
        检查 datasheet 文件夹状态

        Returns:
            {
                'exists': bool,
                'is_empty': bool,
                'files': List[str],
                'message': str
            }
        """
        result = {
            'exists': False,
            'is_empty': True,
            'files': [],
            'message': ''
        }

        # 使用路径解析器获取 datasheet 文件夹
        datasheet_path = self.datasheet_dir

        if not datasheet_path.exists():
            result['message'] = f"❌ datasheet 文件夹不存在！\n请在项目根目录创建: {datasheet_path}"
            return result

        result['exists'] = True

        # 获取所有支持的文件
        files = []
        for ext in self.supported_formats:
            files.extend(datasheet_path.glob(f'*{ext}'))

        result['files'] = [f.name for f in files]
        result['is_empty'] = len(files) == 0

        if result['is_empty']:
            result['message'] = f"⚠️ datasheet 文件夹为空！\n请将芯片手册放入: {datasheet_path}"
        else:
            result['message'] = f"✅ 找到 {len(files)} 个 datasheet 文件"

        return result

    def find_datasheet(self, chip_name: str) -> Optional[Path]:
        """
        根据芯片名称查找 datasheet 文件

        Args:
            chip_name: 芯片型号（如 AT24C02, W25Q128）

        Returns:
            匹配的文件路径，未找到返回 None
        """
        if not self.datasheet_dir.exists():
            return None

        chip_name_lower = chip_name.lower().replace('-', '').replace('_', '')

        for ext in self.supported_formats:
            for file in self.datasheet_dir.glob(f'*{ext}'):
                # 检查文件名是否包含芯片型号
                filename_lower = file.stem.lower().replace('-', '').replace('_', '')
                if chip_name_lower in filename_lower:
                    return file

        return None

    def parse_file(self, file_path: Path) -> Dict[str, Any]:
        """
        解析 datasheet 文件

        Args:
            file_path: 文件路径

        Returns:
            解析结果字典
        """
        suffix = file_path.suffix.lower()

        try:
            if suffix == '.pdf':
                return self._parse_pdf(file_path)
            elif suffix in ['.docx', '.doc']:
                return self._parse_word(file_path)
            elif suffix == '.md':
                return self._parse_markdown(file_path)
            elif suffix in ['.html', '.htm']:
                return self._parse_html(file_path)
            elif suffix == '.txt':
                return self._parse_text(file_path)
            else:
                return {'error': f'不支持的文件格式: {suffix}'}
        except Exception as e:
            return {'error': f'解析失败: {str(e)}'}

    def _parse_pdf(self, file_path: Path) -> Dict[str, Any]:
        """解析 PDF 文件"""
        try:
            import PyPDF2

            text = ""
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"

            # 如果提取的文本太少，可能是扫描件
            if len(text.strip()) < 100:
                return self._ocr_pdf(file_path)

            return self._extract_chip_info(text, file_path.name)

        except ImportError:
            return {'error': '需要安装 PyPDF2: pip install PyPDF2'}
        except Exception as e:
            return {'error': f'PDF 解析失败: {str(e)}'}

    def _ocr_pdf(self, file_path: Path) -> Dict[str, Any]:
        """使用 OCR 解析扫描件 PDF"""
        try:
            import pytesseract
            from pdf2image import convert_from_path

            print("检测到扫描件 PDF，正在使用 OCR 识别...")

            images = convert_from_path(file_path)
            text = ""

            for i, image in enumerate(images):
                page_text = pytesseract.image_to_string(image, lang='eng+chi_sim')
                text += page_text + "\n"

            return self._extract_chip_info(text, file_path.name)

        except ImportError:
            return {'error': '需要安装 OCR 依赖: pip install pytesseract pdf2image pillow'}
        except Exception as e:
            return {'error': f'OCR 识别失败: {str(e)}'}

    def _parse_word(self, file_path: Path) -> Dict[str, Any]:
        """解析 Word 文档"""
        try:
            import docx

            doc = docx.Document(file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])

            return self._extract_chip_info(text, file_path.name)

        except ImportError:
            return {'error': '需要安装 python-docx: pip install python-docx'}
        except Exception as e:
            return {'error': f'Word 解析失败: {str(e)}'}

    def _parse_markdown(self, file_path: Path) -> Dict[str, Any]:
        """解析 Markdown 文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()

            return self._extract_chip_info(text, file_path.name)

        except Exception as e:
            return {'error': f'Markdown 解析失败: {str(e)}'}

    def _parse_html(self, file_path: Path) -> Dict[str, Any]:
        """解析 HTML 文件"""
        try:
            from bs4 import BeautifulSoup

            with open(file_path, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')
                text = soup.get_text()

            return self._extract_chip_info(text, file_path.name)

        except ImportError:
            return {'error': '需要安装 beautifulsoup4: pip install beautifulsoup4'}
        except Exception as e:
            return {'error': f'HTML 解析失败: {str(e)}'}

    def _parse_text(self, file_path: Path) -> Dict[str, Any]:
        """解析纯文本文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()

            return self._extract_chip_info(text, file_path.name)

        except Exception as e:
            return {'error': f'文本解析失败: {str(e)}'}

    def _extract_chip_info(self, text: str, filename: str) -> Dict[str, Any]:
        """
        从文本中提取芯片信息

        Args:
            text: 文档文本内容
            filename: 文件名

        Returns:
            芯片信息字典
        """
        info = {
            'filename': filename,
            'raw_text': text[:5000],  # 保存前5000字符供参考
            'chip_name': self._extract_chip_name(text, filename),
            'interface': self._detect_interface(text),
            'i2c_address': self._extract_i2c_address(text),
            'registers': self._extract_registers(text),
            'voltage': self._extract_voltage(text),
            'features': self._extract_features(text),
        }

        return info

    def _extract_chip_name(self, text: str, filename: str) -> str:
        """提取芯片型号"""
        # 常见芯片型号模式
        patterns = [
            r'([A-Z]{2}\d{2}[A-Z]\d{2})',  # AT24C02, AT24C32 等
            r'(W25Q\d{2,}JV)',  # W25Q128JV 等
            r'(EEPROM\s+[A-Z]+\d+)',  # EEPROM 型号
            r'(Flash\s+[A-Z]+\d+)',  # Flash 型号
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)

        # 从文件名提取
        return filename.split('.')[0]

    def _detect_interface(self, text: str) -> List[str]:
        """检测通信接口类型"""
        interfaces = []
        text_lower = text.lower()

        if 'i2c' in text_lower or 'i²c' in text_lower:
            interfaces.append('I2C')
        if 'spi' in text_lower:
            interfaces.append('SPI')
        if 'uart' in text_lower or 'usart' in text_lower:
            interfaces.append('UART')
        if 'can' in text_lower:
            interfaces.append('CAN')

        return interfaces if interfaces else ['Unknown']

    def _extract_i2c_address(self, text: str) -> List[str]:
        """提取 I2C 地址信息"""
        addresses = []

        # 查找 A0, A0h, 0xA0 等格式
        patterns = [
            r'[Ss]lave\s+[Aa]ddress.*?([0-9A-Fa-f]{2})[hH]',
            r'0x([0-9A-Fa-f]{2}).*?[Dd]evice',
            r'[Dd]evice\s+[Aa]ddress.*?0x([0-9A-Fa-f]{2})',
        ]

        for pattern in patterns:
            matches = re.findall(pattern, text)
            addresses.extend([f'0x{m.upper()}' for m in matches])

        return list(set(addresses))[:5]  # 去重，最多返回5个

    def _extract_registers(self, text: str) -> List[Dict[str, str]]:
        """提取寄存器信息"""
        registers = []

        # 常见寄存器模式
        patterns = [
            r'(\w+)\s+[Rr]egister.*?([0-9A-Fa-f]{2,4})[hH]?',
            r'([0-9A-Fa-f]{2,4})[hH]?\s*-\s*(\w+)',
        ]

        for pattern in patterns:
            matches = re.findall(pattern, text)
            for name, addr in matches:
                if len(name) < 20:  # 过滤掉长文本
                    registers.append({
                        'name': name.strip(),
                        'address': addr.upper()
                    })

        return registers[:10]  # 最多返回10个

    def _extract_voltage(self, text: str) -> List[str]:
        """提取电压规格"""
        voltages = []

        # 电压模式
        pattern = r'(\d+\.?\d*)\s*[Vv]'
        matches = re.findall(pattern, text)

        for v in matches:
            try:
                val = float(v)
                if 1.0 <= val <= 5.5:
                    voltages.append(f"{val}V")
            except:
                pass

        return list(set(voltages))[:3]

    def _extract_features(self, text: str) -> List[str]:
        """提取芯片特性"""
        features = []
        text_lower = text.lower()

        # 容量
        capacity_patterns = [
            r'(\d+)\s*[Kk][Bb]',
            r'(\d+)\s*[Mm][Bb]',
            r'(\d+)\s*-?\s*[Bb]it',
            r'(\d+)\s*Kbit',
        ]

        for pattern in capacity_patterns:
            match = re.search(pattern, text)
            if match:
                features.append(f"容量: {match.group(0)}")
                break

        # 页大小
        page_match = re.search(r'(\d+)\s*-?\s*[Bb]yte\s*/?\s*[Pp]age', text, re.IGNORECASE)
        if page_match:
            features.append(f"页大小: {page_match.group(1)} bytes")

        # 速度
        speed_match = re.search(r'(\d+)\s*[Mm]?\s*[Hh][Zz]', text)
        if speed_match:
            features.append(f"速率: {speed_match.group(0)}")

        return features

    def list_all_datasheets(self) -> List[str]:
        """列出所有可用的 datasheet 文件"""
        result = self.check_datasheet_folder()
        return result['files']

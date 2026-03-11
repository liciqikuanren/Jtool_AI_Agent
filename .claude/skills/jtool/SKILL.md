---
name: jtool-chip-tester
description: 基于 jtool 硬件工具的芯片自动化测试 Skill。当用户需要测试芯片模块、读取/验证芯片寄存器、进行硬件连接测试时触发。支持解析 datasheet（PDF/Word/Markdown/HTML/扫描件）生成测试方案，并执行自动化测试。
---

# JTool 芯片自动化测试 Skill

## 触发场景

当用户提到以下关键词时触发此 Skill：
- "测试芯片"
- "测试 [芯片型号]"
- "读取寄存器"
- "验证硬件"
- "扫描 I2C"
- "检测连接"
- "jtool"
- "硬件测试"

## 工作流程

### Step 1: 检查环境

1. 自动查找 `datasheet` 文件夹（支持多种位置）
2. 自动查找 jtool 可执行文件
3. 检查 jtool 硬件设备是否连接
4. 自动创建 `test_code/` 输出目录

### Step 2: 识别芯片

1. 询问用户要测试的芯片型号
2. 在 `datasheet` 文件夹中搜索匹配的文档
3. 解析文档内容（支持 PDF/Word/Markdown/HTML，扫描件需 OCR）

### Step 3: 生成测试方案

根据 datasheet 分析，生成以下类型的测试方案：
- **连接测试**: I2C/SPI 扫描、设备识别
- **寄存器读取**: 读取芯片 ID、状态寄存器
- **功能测试**: 根据芯片特性设计的功能验证
- **写读验证**: 写入数据后读取验证

### Step 4: 用户确认

使用 `AskUserQuestion` 让用户选择要执行的测试方案。

### Step 5: 执行测试

调用 jtool CMD 或 DLL 执行测试，支持：
- I2C 通信（读写、扫描）
- SPI 通信（读写、命令）
- IO 控制（高低电平、PWM、ADC）

### Step 6: 输出结果

- 生成测试代码（保存到 `test_code/test_[chipname].py`）
- 生成测试报告（保存到 `test_code/report_[chipname]_[timestamp].md`）
- 在对话中展示测试结果

## 目录结构

```
项目根目录/
├── datasheet/                    # 芯片手册文件夹（用户放置）
│   ├── AT24C02.pdf
│   ├── W25Q128JV.pdf
│   └── ...
├── test_code/                    # 测试输出目录（自动生成）
│   ├── test_[chip].py            # 生成的测试代码
│   ├── report_[chip]_[time].md   # 生成的测试报告
│   └── test_example.py           # 示例代码
└── .claude/skills/jtool/
    ├── SKILL.md                  # 本文件
    ├── scripts/
    │   ├── __init__.py
    │   ├── chip_tester.py        # 主测试逻辑
    │   ├── datasheet_parser.py   # 文档解析器
    │   ├── test_executor.py      # 测试执行器
    │   ├── jtool_api.py          # jtool DLL 封装
    │   └── path_resolver.py      # 路径解析器（自动查找资源）
    └── references/
        └── jtool_manual.md       # jtool 完整手册参考
```

## 路径解析（自动查找）

Skill 使用 `path_resolver.py` 自动查找资源，无需硬编码路径：

### 自动查找 jtool
1. 检查 `.claude/skills/jtool/scripts/lib/jtool.exe`
2. 检查 `skills/jtool/scripts/lib/jtool.exe`
3. 检查系统 PATH 中的 `jtool`

### 自动查找 datasheet
1. 检查 `datasheet/`
2. 检查 `datasheets/`
3. 检查 `docs/datasheet/`

### 自动创建输出目录
- 自动在项目根目录创建 `test_code/` 文件夹

## 使用示例

**用户输入**: "帮我测试一下 AT24C02 EEPROM 芯片"

**Skill 响应**:
1. 自动检查环境（jtool、datasheet、输出目录）
2. 在 datasheet 文件夹找到 AT24C02.pdf
3. 解析文档，识别芯片特性：
   - I2C 通信，地址 0xA0
   - 256 字节容量
   - 8 字节页大小
4. 生成测试方案：
   - I2C 连接扫描
   - 读取 Device ID
   - 写入/读取验证
5. 用户选择执行
6. 调用 jtool 执行测试
7. 输出结果和报告到 `test_code/` 目录

## 依赖

- Python 3.8+
- jtool.dll/exe（已放在 scripts/lib/ 目录或系统 PATH）
- 文档解析库：PyPDF2, python-docx, markdown, beautifulsoup4
- OCR：pytesseract（可选，用于扫描件）

## 跨平台兼容性

- **Windows**: 自动查找 `.exe` 文件
- **Linux/macOS**: 自动查找系统 PATH 中的 jtool
- **路径处理**: 使用 `pathlib` 处理不同系统的路径分隔符

## 注意事项

1. 确保 jtool 硬件设备已连接
2. datasheet 文件名应包含芯片型号以便匹配
3. 扫描件需要安装 Tesseract OCR 引擎
4. 生成的测试代码使用 ASCII 字符，避免编码问题

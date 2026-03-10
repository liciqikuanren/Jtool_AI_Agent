---
name: jtool
description: JTool USB适配器硬件测试Skill。当用户提到"测试芯片"、"JTool"、"硬件测试"、"模块测试"、"I2C测试"、"SPI测试"时触发。支持交互式询问芯片型号、管理datasheet手册、生成测试方案并执行测试。
---

# JTool Skill - 硬件测试自动化

Claude Code Skill for JTool USB Adapter Hardware Testing

## 核心功能（根据用户需求实现）

### 1. 主动询问测试模块
Skill 会主动询问用户想要测试的芯片/模块型号，并提供常见类型供选择：
- EEPROM (AT24Cxx系列等)
- 传感器 (温度/湿度/压力等)
- ADC (模数转换器)
- DAC (数模转换器)
- Flash存储器 (SPI Flash)
- GPIO扩展器
- RTC实时时钟

### 2. 数据手册管理
- 提示用户将芯片手册(PDF/TXT)放置到 `datasheet/` 目录
- 自动扫描并列出可用的数据手册
- 支持使用已有手册或添加新手册

### 3. 测试功能选择
根据芯片类型和手册，询问具体要测试的功能：
- 连接测试
- 基本读写测试
- 页写入测试
- 擦除测试
- 自定义功能测试

### 4. 自动生成测试方案并执行
- 根据用户选择生成完整的测试用例
- 自动连接JTool设备
- 执行测试并输出结果报告

---

## 安装

1. 确保项目结构完整：
```
Jtool_AI_Agent/
├── jtool_skill.py                    # Skill入口脚本（根目录）
├── datasheet/                        # 芯片手册目录（根目录）⭐
└── .claude/skills/jtool/
    ├── jtool.yaml                    # Skill定义
    ├── SKILL.md                      # 本文件
    └── scripts/
        ├── lib/
        │   ├── jtool.dll             # JTool驱动
        │   └── jtool.h               # 头文件
        └── src/
            ├── jtool.py              # DLL封装
            ├── test_framework.py     # 测试框架
            ├── jtool_skills.py       # 交互式工具
            └── examples/             # 测试示例
```

2. **重要**: 将你的芯片数据手册(PDF/TXT)放入根目录的 `datasheet/` 文件夹

---

## 使用方法

### 方式1: 使用 /skills 命令

```bash
# 启动交互式测试向导（推荐）
/skills jtool

# 扫描设备
/skills jtool scan

# 快速测试
/skills jtool quick

# 测试EEPROM
/skills jtool test-eeprom

# 测试Flash
/skills jtool test-flash
```

### 方式2: 直接运行Python脚本

```bash
# 交互式模式（完整6步流程）
python jtool_skill.py

# 扫描设备
python jtool_skill.py scan

# 快速I2C测试
python jtool_skill.py quick

# 测试EEPROM (指定地址)
python jtool_skill.py test-eeprom --addr 0x50
```

---

## 交互式测试流程（6步向导）

```
┌─────────────────────────────────────────────────────────────┐
│  步骤1: 询问模块                                             │
│  ├── 选择模块类型 (EEPROM/传感器/Flash等)                     │
│  └── 输入具体芯片型号 (如 AT24C02, W25Q128)                   │
├─────────────────────────────────────────────────────────────┤
│  步骤2: 检查数据手册                                          │
│  ├── 扫描 datasheet/ 目录                                    │
│  ├── 提示用户放置手册 (如需要)                                 │
│  └── 选择要使用的手册                                        │
├─────────────────────────────────────────────────────────────┤
│  步骤3: 选择通信接口                                          │
│  ├── I2C (推荐用于EEPROM/传感器)                              │
│  ├── SPI (推荐用于Flash/ADC)                                  │
│  ├── GPIO                                                    │
│  └── CAN                                                     │
├─────────────────────────────────────────────────────────────┤
│  步骤4: 选择测试功能                                          │
│  ├── 根据芯片类型列出可用测试项                                │
│  └── 用户选择要执行的测试                                     │
├─────────────────────────────────────────────────────────────┤
│  步骤5: 配置设备参数                                          │
│  ├── I2C: 设备地址、页大小                                    │
│  └── SPI: 模式、时钟频率                                      │
├─────────────────────────────────────────────────────────────┤
│  步骤6: 生成并执行测试                                        │
│  ├── 自动生成测试方案                                        │
│  ├── 执行测试                                                │
│  └── 生成测试报告                                            │
└─────────────────────────────────────────────────────────────┘
```

---

## Skill功能

| 命令 | 说明 |
|------|------|
| `interactive` | 交互式测试向导（完整6步流程） |
| `scan` | 扫描所有连接的JTool设备 |
| `quick` | 快速I2C总线扫描和设备检测 |
| `test-eeprom` | AT24C02 EEPROM完整测试 |
| `test-flash` | W25Q SPI Flash完整测试 |

---

## 扩展开发

### 添加新的芯片测试模板

编辑 `.claude/skills/jtool/scripts/src/test_framework.py`，在 `CHIP_TEMPLATES` 中添加：

```python
"my_chip": {
    "interface": InterfaceType.I2C,
    "test_cases": [
        "连接测试",
        "寄存器读取",
        "功能测试"
    ]
}
```

### 添加新的测试用例生成器

在 `TestPlanGenerator` 类中添加：

```python
@classmethod
def _create_my_chip_test_case(cls, test_name: str, chip_info: Optional[Dict]) -> TestCase:
    return TestCase(
        name=test_name,
        description="测试说明",
        interface=InterfaceType.I2C,
        setup_steps=[],
        test_steps=[{"action": "i2c_write", ...}],
        expected_result="期望结果"
    )
```

---

## 文件结构

```
.
├── jtool_skill.py                          # Skill入口（根目录）
├── datasheet/                              # 芯片手册目录（根目录）⭐
│   ├── AT24C02.pdf
│   ├── W25Q128.pdf
│   └── ...
└── .claude/skills/jtool/
    ├── jtool.yaml                          # Skill定义
    ├── SKILL.md                            # 本文件
    └── scripts/
        ├── lib/
        │   ├── jtool.dll                   # JTool驱动
        │   └── jtool.h                     # 头文件
        └── src/
            ├── jtool.py                    # DLL封装
            ├── test_framework.py           # 测试框架
            ├── jtool_skills.py             # 交互式工具（6步向导）
            ├── scan_devices.py             # 设备扫描
            ├── README.md                   # 源码文档
            └── examples/
                ├── test_eeprom_at24c02.py  # EEPROM测试
                └── test_flash_w25q.py      # Flash测试
```

---

## 依赖

- Python 3.7+
- Windows系统（JTool DLL为Windows x64版本）
- JTool USB适配器硬件

## 注意事项

1. 确保JTool设备已正确连接到USB
2. 确保目标芯片已正确连接到JTool适配器
3. 将芯片数据手册放置到 `datasheet/` 目录以获得更好体验
4. 部分测试会修改设备数据，请谨慎在生产环境使用

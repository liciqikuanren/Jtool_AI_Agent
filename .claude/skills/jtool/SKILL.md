# JTool Skill

Claude Code Skill for JTool USB Adapter Hardware Testing

## 安装

1. 确保项目结构完整：
```
Jtool_AI_Agent/
├── jtool_skill.py                    # Skill入口脚本（根目录）
└── .claude/skills/jtool/
    ├── jtool.yaml                    # Skill定义
    ├── SKILL.md                      # 本文件
    ├── assets/
    │   └── datasheet/                # 数据手册目录（PDF/TXT）
    └── scripts/
        ├── lib/
        │   ├── jtool.dll             # JTool驱动
        │   └── jtool.h               # 头文件
        └── src/
            ├── jtool.py              # DLL封装
            ├── test_framework.py     # 测试框架
            ├── jtool_skills.py       # 交互式工具
            ├── scan_devices.py       # 设备扫描
            └── examples/             # 测试示例
```

2. Skill会自动被Claude Code识别，无需额外安装

## 使用方法

### 方式1: 使用 /skills 命令

```bash
# 启动交互式测试向导
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
# 交互式模式
python jtool_skill.py

# 扫描设备
python jtool_skill.py scan

# 测试EEPROM (指定地址)
python jtool_skill.py test-eeprom --addr 0x50
```

## Skill功能

| 命令 | 说明 |
|------|------|
| `interactive` | 交互式测试向导，询问芯片类型并生成测试方案 |
| `scan` | 扫描所有连接的JTool设备 |
| `quick` | 快速I2C总线扫描和设备检测 |
| `test-eeprom` | AT24C02 EEPROM完整测试 |
| `test-flash` | W25Q SPI Flash完整测试 |

## 交互式测试流程

1. **选择模块类型** - EEPROM/传感器/Flash/GPIO扩展器等
2. **检查数据手册** - 提示放置PDF到 `.claude/skills/jtool/assets/datasheet/` 目录
3. **选择通信接口** - I2C/SPI/GPIO
4. **选择测试项目** - 连接测试/读写测试/功能测试等
5. **配置参数** - 设备地址、SPI模式等
6. **执行测试** - 自动生成并运行测试方案
7. **查看报告** - 显示测试结果并可选保存

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

## 文件结构

```
.
├── jtool_skill.py                          # Skill入口（根目录）
└── .claude/skills/jtool/
    ├── jtool.yaml                          # Skill定义
    ├── SKILL.md                            # 本文件
    ├── assets/
    │   └── datasheet/                      # 数据手册目录
    └── scripts/
        ├── lib/
        │   ├── jtool.dll                   # JTool驱动
        │   └── jtool.h                     # 头文件
        └── src/
            ├── jtool.py                    # DLL封装
            ├── test_framework.py           # 测试框架
            ├── jtool_skills.py             # 交互式工具
            ├── scan_devices.py             # 设备扫描
            ├── README.md                   # 源码文档
            └── examples/
                ├── test_eeprom_at24c02.py  # EEPROM测试
                └── test_flash_w25q.py      # Flash测试
```

## 依赖

- Python 3.7+
- Windows系统（JTool DLL为Windows x64版本）
- JTool USB适配器硬件

## 注意事项

1. 确保JTool设备已正确连接到USB
2. 确保目标芯片已正确连接到JTool适配器
3. 部分测试会修改设备数据，请谨慎在生产环境使用

# JTool Python 测试框架

基于JTool USB适配器的硬件测试自动化工具包。

## 文件结构

```
src/
├── __init__.py           - 包初始化
├── jtool.py              - JTool DLL封装和底层API
├── test_framework.py     - 测试框架和测试方案生成器
├── jtool_skills.py       - 交互式测试工具（主入口）
├── scan_devices.py       - 设备扫描工具
├── examples/             - 示例测试脚本
│   ├── test_eeprom_at24c02.py  - AT24C02 EEPROM测试
│   └── test_flash_w25q.py      - W25Q Flash测试
```

## 使用说明

### 1. 交互式测试模式

启动交互式测试向导，根据提示完成测试：

```bash
python -m src.jtool_skills
```

或

```bash
python src/jtool_skills.py
```

流程：
1. 选择要测试的模块类型（EEPROM/传感器/Flash等）
2. 检查数据手册（提示放置到`datasheet/`目录）
3. 选择通信接口（I2C/SPI/GPIO）
4. 选择要执行的测试项目
5. 配置设备参数（地址、模式等）
6. 生成并执行测试方案

### 2. 快速扫描设备

扫描所有连接的JTool设备：

```bash
python -m src.scan_devices
```

### 3. 直接编程使用

```python
from jtool import open_i2c_device, RegAddrType
from test_framework import TestExecutor, TestPlanGenerator

# 打开I2C设备
handle, i2c = open_i2c_device()

# 扫描总线
count, addresses = i2c.scan()
print(f"发现 {count} 个设备")

# 读写数据
i2c.write(0x50, RegAddrType.BIT8, 0x00, b'\xAA\xBB')
data = i2c.read(0x50, RegAddrType.BIT8, 0x00, 2)
```

### 4. 运行示例测试

```bash
# 测试AT24C02 EEPROM
python -m src.examples.test_eeprom_at24c02

# 测试W25Q Flash
python -m src.examples.test_flash_w25q
```

## 支持的接口

### I2C
- 设备扫描
- 字节/页读写
- EEPROM专用操作（自动分页）

### SPI
- 标准SPI读写
- QSPI支持
- 带命令/地址的传输

### GPIO
- 输入/输出配置
- PWM输出
- ADC输入
- 频率/占空比捕获
- 脉冲生成

## 数据手册管理

将芯片数据手册放在项目根目录的`datasheet/`文件夹中：

```
datasheet/
├── AT24C02.pdf
├── BMP280.pdf
└── W25Q128.pdf
```

交互式工具会自动识别并提示使用。

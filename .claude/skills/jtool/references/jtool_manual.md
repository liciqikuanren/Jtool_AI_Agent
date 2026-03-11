# JTool CMD/DLL 参考手册

## 简介

JTool 提供命令行工具和 DLL API，用于：
- USB 转 I2C 通信
- USB 转 SPI 通信
- USB 转 IO 控制

## CMD 命令集

### 通用命令

```bash
# 查看帮助
jtool --help

# 扫描设备
jtool scan

# 延时（ms）
jtool delay 1000
```

### JIO 命令（IO 控制）

```bash
# IO 置高
jtool ioh 1
jtool ioh -i 0 1        # 指定设备 ID 0
jtool ioh -m 0x0f       # 多通道（IO1-IO4）

# IO 置低
jtool iol 1
jtool iol -m 0x0f

# IO 读写
jtool iow 1 0           # IO1 写低
jtool iow 1 1           # IO1 写高
jtool ior 1             # 读取 IO1 电平

# PWM 输出
jtool pwmon 1 500       # IO1 输出 50% 占空比 PWM
jtool pwmoff 1          # 关闭 IO1 PWM
jtool pwmfreq 1000      # 设置 PWM 频率 1KHz

# 脉冲输出
jtool pulseon 1 400000  # IO1 输出 400KHz 脉冲
jtool pulseoff 1        # 停止脉冲
jtool pulsecnt 1 1000 100000  # 输出 1000 个 100KHz 脉冲

# ADC 采样
jtool adcon 1 0         # 开启 IO1 ADC（单端）
jtool adcget 1          # 获取 IO1 ADC 值

# PWM 捕获（仅通道1）
jtool capon 1           # 开启捕获
jtool capget 1          # 获取捕获值
jtool capclear 1        # 清空计数
```

### JI2C 命令（I2C 通信）

```bash
# 扫描 I2C 设备
jtool i2cscan
jtool i2cscan -s        # 7 位地址模式
jtool i2cscan -i 0      # 指定设备 ID

# I2C 写数据
jtool i2cwrite A0 00 11 22 33 44 55
#        从机地址 寄存器 数据...

# I2C 读数据
jtool i2cread A0 00 16
#        从机地址 寄存器 长度

# EEPROM 写（自动跨页处理）
jtool eewrite -p 8 A0 00 11 22 33 44 55
#           页大小 从机地址 寄存器 数据...

# EEPROM 读
jtool eeread A0 00 16

# EEPROM 写文件
jtool eewritef -p 8 A0 00 ./data.bin

# EEPROM 读文件
jtool eereadf A0 00 256 ./output/

# 中断检测
jtool i2cint 1          # 检测上升沿中断
jtool i2cint -w 1       # 等待中断后退出

# 设备控制
jtool ji2cvcc 0         # VCC = 5V
jtool ji2cvcc 1         # VCC = VIO
jtool ji2cvcc 2         # VCC 关闭
jtool ji2cvio 0         # VIO = 3.3V
jtool ji2cvio 1         # VIO = 1.8V
jtool ji2cspd 2         # I2C 速率 100K
jtool ji2creboot        # 重启设备
```

### JSPI 命令（SPI 通信）

```bash
# SPI 仅写
jtool spiwrite 00 01 02 03 04 05
jtool spiwrite -m 2 -e 1 00 01 02  # 模式2, LSB

# SPI 仅读
jtool spiread 5

# SPI 写同时读
jtool spiwr 00 01 02 03

# QSPI 读写
jtool qspiwrite 00 01 02
jtool qspiread 5

# 带指令的 SPI 读写
jtool spiwcmd -c 01 -a 0000 55 55 55
#           指令  地址   数据

jtool spircmd -c 01 -a 0000 16
#           指令  地址   读取长度

# SPI 模式设置
# -m 0: LOW_1EDG, 1: LOW_2EDG, 2: HIGH_1EDG, 3: HIGH_2EDG
# -e 0: MSB, 1: LSB
# -q 0: 全单线, 1: 全四线, 2: 数据四线, 3: 指令单线

# 设备控制
jtool jspivcc 0         # VCC = 5V
jtool jspivio 0         # VIO = 3.3V
jtool jspispd 21        # SPI 速率 937.5K
jtool jspireboot        # 重启设备
```

## DLL API 接口

### 设备类型枚举

```c
typedef enum {
    dev_all = -1,
    dev_i2c = 0,
    dev_io,
    dev_spi,
    dev_can,
    dev_max,
} dev_type_enum;
```

### 错误类型枚举

```c
typedef enum {
    ErrNone = 0,        // 成功
    ErrParam = 1,       // 参数错误
    ErrDisconnect = 2,  // USB 断开
    ErrBusy = 4,        // USB 发送忙
    ErrWaiting = 8,     // 正在等待回复
    ErrTimeOut = 16,    // 通信超时
    ErrDataParse = 32,  // 通信数据错误
    ErrFailACK = 64,    // 返回失败参数
} ErrorType;
```

### 寄存器地址类型

```c
typedef enum {
    REGADDR_NONE = 0,   // 不发送地址
    REGADDR_8Bit = 1,   // 8 位地址
    REGADDR_16Bit = 2,  // 16 位地址
    REGADDR_24Bit = 3,  // 24 位地址
    REGADDR_32Bit = 4,  // 32 位地址
} REGADDR_TYPE;
```

### 公共 API

```c
// 扫描设备
char* DevicesScan(int DevType, int* OutCnt);

// 打开设备
void* DevOpen(int DevType, char* Sn, int Id);

// 关闭设备
BOOL DevClose(void* DevHandle);
```

### JIO API

```c
// IO 设置
ErrorType IOSetNone(void* DevHandle, uint32_t ionum);
ErrorType IOSetIn(void* DevHandle, uint32_t ionum, BOOL pullup, BOOL pulldown);
ErrorType IOSetOut(void* DevHandle, uint32_t ionum, BOOL pp);
ErrorType IOSetVal(void* DevHandle, uint32_t ionum, BOOL val);

// PWM
ErrorType PWMSetFreq(void* DevHandle, uint32_t freq);
ErrorType PWMSetOn(void* DevHandle, uint32_t ionum);
ErrorType PWMSetOff(void* DevHandle, uint32_t ionum);
ErrorType PWMSetDuty(void* DevHandle, uint32_t ionum, uint32_t duty);

// 脉冲
ErrorType IOPulseOn(void* DevHandle, uint32_t ionum, uint32_t freq);
ErrorType IOPulseOff(void* DevHandle, uint32_t ionum);
ErrorType IOPulseCnt(void* DevHandle, uint32_t ionum, uint32_t cnt, uint32_t freq);

// ADC
ErrorType ADCSetIn(void* DevHandle, uint32_t ionum);
ErrorType ADCSetSamp(void* DevHandle, uint32_t freq);
int32_t ADCGetVal(void* DevHandle, uint32_t ionum);

// 读取
ErrorType IOGetInVal(void* DevHandle, uint32_t ionum);
ErrorType CapGetVal(void* DevHandle, uint32_t ionum);
```

### JI2C API

```c
// 扫描
int I2CScan(void* DevHandle);

// 读写
int I2CWrite(void* DevHandle, byte slave_addr, int reg_type,
             uint32_t reg_addr, uint16_t len, byte* buf);
int I2CRead(void* DevHandle, byte slave_addr, int reg_type,
            uint32_t reg_addr, uint16_t len, byte* buf);

// EEPROM
int EEWrite(void* DevHandle, byte slave_addr, int reg_type,
            uint32_t reg_addr, uint16_t pagesize, uint16_t len, byte* buf);
int EERead(void* DevHandle, byte slave_addr, int reg_type,
           uint32_t reg_addr, uint16_t len, byte* buf);

// 中断
typedef void (*I2CIntCallbackFun)(void);
void I2CRegisterIntCallback(I2CIntCallbackFun fun);
void I2CCloseIntCallback(void);
```

### JSPI API

```c
// 基本 SPI
int SPIWriteOnly(void* DevHandle, uint16_t len, byte* buf);
int SPIReadOnly(void* DevHandle, uint16_t len, byte* buf);
int SPIWriteRead(void* DevHandle, uint16_t len, byte* buf);

// QSPI
int QSPIWriteOnly(void* DevHandle, uint16_t len, byte* buf);
int QSPIReadOnly(void* DevHandle, uint16_t len, byte* buf);

// 带指令
int SPIWriteWithCMD(void* DevHandle, byte* cmd, int cmd_len,
                    byte* addr, int addr_len, byte* alt, int alt_len,
                    int dummy_len, uint16_t len, byte* buf);
int SPIReadWithCMD(void* DevHandle, byte* cmd, int cmd_len,
                   byte* addr, int addr_len, byte* alt, int alt_len,
                   int dummy_len, uint16_t len, byte* buf);

// 中断
typedef void (*SPIIntCallbackFun)(void);
void SPIRegisterIntCallback(SPIIntCallbackFun fun);
void SPICloseIntCallback(void);
```

## 常用芯片测试示例

### AT24C02 EEPROM 测试

```bash
# 1. I2C 扫描
jtool i2cscan -s

# 2. 读取数据（从地址 0x00 读 16 字节）
jtool i2cread A0 00 16

# 3. 写入数据
jtool i2cwrite A0 00 11 22 33 44 55 66 77 88

# 4. 再次读取验证
jtool i2cread A0 00 10
```

### W25Q Flash 测试

```bash
# 1. 读取 JEDEC ID
jtool spircmd -c 9F 3

# 2. 读取状态寄存器
jtool spircmd -c 05 1

# 3. 读取数据（从地址 0x000000 读 16 字节）
jtool spircmd -c 03 -a 000000 16
```

## 注意事项

1. **设备占用**: 打开设备后，其他进程无法再次打开，直到调用 `DevClose` 或进程退出
2. **EEPROM 写入**: 需要等待写入完成（约 5-10ms）后才能读取
3. **I2C 地址**: 命令行中使用不包含读写位的地址（如 A0）
4. **SPI 模式**: 默认模式 0（CPOL=0, CPHA=0）

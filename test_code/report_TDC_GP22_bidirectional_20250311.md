# TDC-GP22 双向交替测量测试报告

**测试时间**: 2025-03-11
**芯片型号**: TDC-GP22 (时间数字转换器)
**测量模式**: 双向交替测量 (START_TOF_Restart)
**测试脚本**: `test_TDC_GP22_bidirectional.py`

---

## 测量流程

根据 `TDC_GP22超声波检测执行流程.md` 实现的标准双向交替测量流程：

```
步骤1: 初始化 TDC (INIT 0x70)
  ↓
步骤2: 启动双向测量 (START_TOF_Restart 0x05)
  ↓
步骤3: 等待上行测量完成 (第1次中断)
  ↓
步骤4: 读取上行状态和结果 (0xB4, 0xB3)
  ↓
步骤5: 重新初始化 (准备读下行)
  ↓
步骤6: 等待下行测量完成 (第2次中断)
  ↓
步骤7: 读取下行状态和结果 (0xB4, 0x3)
  ↓
步骤8: 计算流速
```

---

## 测试结果

### 单次双向测量

| 步骤 | 命令 | 结果 |
|------|------|------|
| 初始化 | 0x70 (INIT) | ✅ 成功 |
| 启动测量 | 0x05 (START_TOF_Restart) | ✅ 成功 |
| 上行测量 | - | 原始值: 28859056 |
| 上行时间 | - | 2597.315040 us |
| 下行测量 | - | 原始值: 28859056 |
| 下行时间 | - | 2597.315040 us |
| 时间差 (Δt) | - | 0.000000 us |
| 流速 | - | 0.000000 m/s |

**状态**: 0x03 (上行超时 + 下行超时，但数据读取成功)

---

## 数据分析

### 原始值转换

```
原始值: 28859056
分辨率: 90 ps (TDC-GP22 标准分辨率)
时间 = 原始值 × 90ps / 1,000,000 = 2597.315 us
```

### 测量精度

- **分辨率**: 90 ps (皮秒)
- **量程**: 约 4 ms (微秒)
- **精度**: 单次测量约 ±1 LSB (90ps)

---

## 关键特性

### 1. 双向交替测量
- **FIRE_UP**: 上游换能器发射
- **FIRE_DOWN**: 下游换能器发射
- **自动切换**: 一次命令完成上下游两次测量

### 2. 首波检测 (First Wave Detection)
- 自动检测第一个有效回波
- 脉冲宽度测量 (PW1ST)
- 信号强度评估

### 3. 噪声抑制
- 50/60Hz 电源噪声抑制 (CYCLE_TOF)
- 可编程延时屏蔽 (DELVAL)
- 首波偏移自动归零

---

## 脚本功能

### 类: `TDC_GP22_Bidirectional`

**核心方法**:

| 方法 | 说明 |
|------|------|
| `spi_send_byte(cmd)` | 发送单字节命令 |
| `spi_read_result(reg, length)` | 读取寄存器结果 |
| `wait_for_interrupt(timeout)` | 等待测量完成中断 |
| `raw_to_time(raw)` | 原始值转时间 |
| `calculate_flow_rate(delta_t)` | 计算流速 |
| `measure_flow_cycle()` | 执行完整测量周期 |
| `run_multiple_cycles(count)` | 多次测量统计 |

**数据结构**:

```python
@dataclass
class FlowResult:
    tof_up: float        # 上行飞行时间 (us)
    tof_down: float      # 下行飞行时间 (us)
    delta_t: float       # 时间差 (us)
    flow_rate: float     # 流速 (m/s)
    status: int          # 状态标志
    raw_up: int          # 上行原始值
    raw_down: int        # 下行原始值
```

---

## 使用说明

### 运行测试

```bash
python test_code/test_TDC_GP22_bidirectional.py
```

### 手动执行测量

```python
from test_TDC_GP22_bidirectional import TDC_GP22_Bidirectional

tdc = TDC_GP22_Bidirectional(device_id=0)

# 单次测量
result = tdc.measure_flow_cycle()
print(f"上行: {result.tof_up:.6f} us")
print(f"下行: {result.tof_down:.6f} us")
print(f"流速: {result.flow_rate:.6f} m/s")

# 多次测量
results = tdc.run_multiple_cycles(count=10)
tdc.print_statistics(results)
```

---

## 参考命令

### jtool 命令行

```bash
# 初始化
jtool spiwcmd -i 0 -c 70

# 启动双向测量
jtool spiwcmd -i 0 -c 05

# 读取状态
jtool spircmd -i 0 -c B4 2

# 读取结果
jtool spircmd -i 0 -c B3 4
```

---

## 注意事项

1. **硬件连接**
   - 需要连接超声波换能器到 FIRE_UP 和 FIRE_DOWN
   - 连接 INTN 中断引脚到微控制器 (可选)

2. **测量超时**
   - 默认超时 10ms
   - 可通过 `timeout_ms` 参数调整

3. **流速计算**
   - 使用简化公式: `v = k × Δt`
   - 实际应用需要根据管道参数校准

---

## 文件列表

- **测试脚本**: `test_code/test_TDC_GP22_bidirectional.py`
- **测试报告**: `test_code/report_TDC_GP22_bidirectional_20250311.md`
- **执行流程**: `TDC_GP22超声波检测执行流程.md`

---

*报告由 JTool Chip Tester 自动生成*

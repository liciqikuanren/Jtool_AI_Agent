## **二、超声波检测完整流程**

### **1. 单次测量流程（START_TOF）**



```
时序图：
  ┌─────────────────────────────────────────────────────┐
  │ 微控制器              │ TDC-GP22内部               │
  ├─────────────────────────────────────────────────────┤
  │ 发送INIT(0x70)       │ 复位TDC，准备接收START     │
  │ 发送START_TOF(0x01)  │ 开始测量序列              │
  │                      │ 1. 开启4MHz振荡器          │
  │                      │ 2. 等待480µs（陶瓷谐振器） │
  │                      │ 3. 开启比较器、参考电压    │
  │                      │ 4. 充电接收电容（TW2=300µs）│
  │                      │ 5. 发送FIRE脉冲（10个）    │
  │                      │ 6. 开启STOP通道（DELVAL后）│
  │                      │ 7. 等待回波信号            │
  │                      │ 8. 测量完成，关闭模拟部分  │
  │                      │ 9. 设置INTN=LOW           │
  │ 检测INTN=LOW        │                            │
  │ 读取状态(0xB4)      │                            │
  │ 读取结果(0xB3)      │ 返回飞行时间              │
  └─────────────────────────────────────────────────────┘
```

**代码实现：**

c



```
float single_tof_measurement(void) {
    float tof_result = 0;
    
    // 阶段1：准备测量
    spi_send_byte(0x70);        // INIT
    delay_us(10);
    
    // 阶段2：启动测量
    spi_send_byte(0x01);        // START_TOF
    
    // 阶段3：等待测量完成（最长4ms）
    uint32_t start_time = get_tick_count();
    while(GPIO_Read(INTN_PIN) == HIGH) {
        if(get_tick_count() - start_time > 5) {  // 5ms超时
            return -1.0;  // 超时错误
        }
    }
    
    // 阶段4：读取状态检查错误
    uint16_t status = spi_read_result(0xB4);
    if(status & 0x0600) {       // 检查超时或错误
        handle_measurement_error(status);
        return -1.0;
    }
    
    // 阶段5：读取结果
    uint32_t raw_result = spi_read_result(0xB3);
    
    // 阶段6：转换为时间（考虑校准）
    tof_result = raw_to_time(raw_result);
    
    return tof_result;
}
```

### **2. 双向交替测量流程（START_TOF_Restart）**



```
这是超声波流量计的标准流程，自动完成上下游测量：

流程详解：
  第1阶段：上行测量（FIRE_UP激活）
    ┌─ 微控制器发送0x05（START_TOF_Restart）
    ├─ TDC-GP22执行：
    │   1. 配置FIRE_UP为活动输出
    │   2. 执行完整测量序列（同上）
    │   3. 测量完成，INTN=LOW（第1次中断）
    └─ 微控制器读取上行结果
    
  第2阶段：等待周期（抑制50/60Hz噪声）
    ┌─ TDC-GP22自动等待CYCLE_TOF×20ms
    │  （CYCLE_TOF=0时等待20ms@50Hz）
    └─ 期间微控制器可处理上行数据
    
  第3阶段：下行测量（FIRE_DOWN激活）
    ┌─ TDC-GP22自动开始：
    │   1. 配置FIRE_DOWN为活动输出
    │   2. 执行完整测量序列
    │   3. 测量完成，INTN=LOW（第2次中断）
    └─ 微控制器读取下行结果
```

**代码实现：**

c



```
typedef struct {
    float tof_up;      // 上行飞行时间
    float tof_down;    // 下行飞行时间  
    float flow_rate;   // 计算出的流速
    uint8_t status;    // 状态标志
} flow_measurement_t;

flow_measurement_t measure_flow_cycle(void) {
    flow_measurement_t result = {0};
    
    // 步骤1：初始化TDC
    spi_send_byte(0x70);        // INIT
    
    // 步骤2：启动双向测量
    spi_send_byte(0x05);        // START_TOF_Restart
    
    // 步骤3：等待第1次中断（上行完成）
    wait_for_interrupt(5);      // 5ms超时
    if(timeout) {
        result.status |= FLOW_TIMEOUT_UP;
        return result;
    }
    
    // 步骤4：读取上行状态和结果
    uint16_t stat_up = spi_read_result(0xB4);
    if(stat_up & 0x0600) {
        result.status |= FLOW_ERROR_UP;
        // 但仍继续，可能下行正常
    }
    uint32_t raw_up = spi_read_result(0xB3);
    result.tof_up = raw_to_time(raw_up);
    
    // 步骤5：重新初始化（准备读下行）
    spi_send_byte(0x70);        // INIT
    
    // 步骤6：等待第2次中断（下行完成）
    wait_for_interrupt(5);      // 5ms超时
    if(timeout) {
        result.status |= FLOW_TIMEOUT_DOWN;
        return result;
    }
    
    // 步骤7：读取下行状态和结果
    uint16_t stat_down = spi_read_result(0xB4);
    if(stat_down & 0x0600) {
        result.status |= FLOW_ERROR_DOWN;
    }
    uint32_t raw_down = spi_read_result(0xB3);
    result.tof_down = raw_to_time(raw_down);
    
    // 步骤8：计算流速
    if(!(result.status & (FLOW_ERROR_UP | FLOW_ERROR_DOWN))) {
        float delta_t = result.tof_down - result.tof_up;
        result.flow_rate = calculate_flow_rate(delta_t);
    }
    
    return result;
}
```

### **3. 首波检测模式详细流程**



```
这是TDC-GP22的核心改进功能，确保可靠检测：

时序细节：
  T0: FIRE脉冲发出，START计时开始
  T0+DELVAL1: 开启STOP通道（粗略屏蔽噪声）
  
  首波检测阶段：
    T1: 接收信号超过偏移阈值（如+30mV）
    T1+立即: 测量首波脉冲宽度（上升沿到下降沿）
    T1+立即: 偏移自动归零（<1mV）
    
  正式测量阶段：
    T1+DELREL1×周期: 测量第1个正式波（如第8个波）
    T1+DELREL2×周期: 测量第2个正式波（如第9个波）
    T1+DELREL3×周期: 测量第3个正式波（如第10个波）
    
  数据处理：
    自动计算3个结果的平均值
    存储到RES_3寄存器
    脉冲宽度比值存储到PW1ST寄存器
```

**首波检测配置代码：**



c



```
void configure_first_wave_mode(void) {
    // 关键配置参数
    uint32_t reg3 = 0;
    
    // 启用首波检测
    reg3 |= (1 << 30);          // EN_FIRST_WAVE = 1
    
    // 启用自动计算
    reg3 |= (1 << 31);          // EN_AUTOALC_MB2 = 1
    
    // 设置测量波序（测量第8、9、10个波）
    reg3 |= (8 << 8);           // DELREL1 = 8
    reg3 |= (9 << 14);          // DELREL2 = 9  
    reg3 |= (10 << 20);         // DELREL3 = 10
    
    // 设置超时（4ms @ 4MHz）
    reg3 |= (3 << 27);          // SEL_TIMO_MB2 = 3（4096µs）
    
    spi_write_reg(0x83, reg3);
    
    // 配置脉冲宽度测量
    uint32_t reg4 = 0;
    reg4 &= ~(1 << 16);         // DIS_PW = 0（启用）
    reg4 &= ~(1 << 15);         // EDGE_FW = 0（上升沿）
    reg4 |= (0x4A << 8);        // OFFS=10, OFFSRNG2=1（总30mV）
    
    spi_write_reg(0x84, reg4);
}
```
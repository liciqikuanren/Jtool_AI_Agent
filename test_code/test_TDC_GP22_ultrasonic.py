"""
TDC-GP22 超声波水表测试程序
功能: 交替发波模式，一次发波 20 个脉冲
生成时间: 2025-03-11
"""

import subprocess
import sys
import time
from pathlib import Path
from typing import List, Tuple, Dict
from datetime import datetime


def get_jtool_path() -> str:
    """获取 jtool 可执行文件路径"""
    possible_paths = [
        Path(__file__).parent.parent / ".claude" / "skills" / "jtool" / "scripts" / "lib" / "jtool.exe",
        Path(".claude/skills/jtool/scripts/lib/jtool.exe"),
        Path("jtool.exe"),
        "jtool",
    ]
    for path in possible_paths:
        if isinstance(path, Path) and path.exists():
            return str(path)
    return "jtool"


class TDC_GP22_Ultrasonic:
    """
    TDC-GP22 超声波水表测试类

    支持功能:
    - 交替发波模式 (Alternating Mode)
    - 可配置脉冲数量
    - 时间测量
    - 温度测量
    """

    # TDC-GP22 配置寄存器地址 (用于写入, opcode 0x8x)
    REG_CONFIG_0 = "00"      # 配置寄存器 0
    REG_CONFIG_1 = "01"      # 配置寄存器 1
    REG_CONFIG_2 = "02"      # 配置寄存器 2
    REG_CONFIG_3 = "03"      # 配置寄存器 3
    REG_CONFIG_4 = "04"      # 配置寄存器 4
    REG_CONFIG_5 = "05"      # 配置寄存器 5
    REG_CONFIG_6 = "06"      # 配置寄存器 6

    # TDC-GP22 读取寄存器 opcode (用于读取, opcode 0xBx)
    # 注意: 读取时使用 B0-B6, 状态用 B4, 结果用 B0-B3
    REG_READ_0 = "0"         # 读取配置寄存器 0 (opcode 0xB0)
    REG_READ_1 = "1"         # 读取配置寄存器 1 (opcode 0xB1)
    REG_READ_2 = "2"         # 读取配置寄存器 2 (opcode 0xB2)
    REG_READ_3 = "3"         # 读取配置寄存器 3 / 结果 RES_3 (opcode 0xB3)
    REG_STATUS = "4"         # 状态寄存器 (opcode 0xB4)
    REG_RES_0 = "0"          # 结果寄存器 0 (opcode 0xB0)
    REG_RES_1 = "1"          # 结果寄存器 1 (opcode 0xB1)
    REG_RES_2 = "2"          # 结果寄存器 2 (opcode 0xB2)
    REG_RES_3 = "3"          # 结果寄存器 3 (opcode 0xB3)

    # 测量模式
    MODE_1 = 1    # 测量模式 1: 单一测量
    MODE_2 = 2    # 测量模式 2: 交替测量 (用于水表)

    def __init__(self, device_id: int = 0):
        self.chip_name = "TDC-GP22"
        self.jtool = get_jtool_path()
        self.device_id = device_id
        self.results = []

        # 默认配置: 交替发波模式，20 脉冲
        self.pulse_count = 20

    def check_spi_connection(self) -> Dict:
        """
        检测 SPI 连接状态

        Returns:
            检测结果字典
        """
        result = {
            'test_name': 'SPI Connection Check',
            'success': False,
            'device_found': False,
            'spi_ok': False,
            'messages': [],
        }

        print("\n" + "=" * 60)
        print("SPI 连接检测")
        print("=" * 60)

        # 1. 扫描 jtool 设备
        print("\n[1/3] 扫描 jtool 设备...")
        returncode, output = self.run_command(['scan'])

        if returncode == 0 and 'JTool-SPI' in output:
            result['device_found'] = True
            result['messages'].append(f"[OK] 找到 SPI 设备: {output.strip()}")
            print(f"  [OK] {output.strip()}")
        else:
            result['messages'].append(f"[FAIL] 未找到 SPI 设备: {output}")
            print(f"  [FAIL] {output}")
            return result

        # 2. 测试 SPI 读取
        print("\n[2/3] 测试 SPI 读取...")
        returncode, output = self.run_command([
            'spircmd', '-i', str(self.device_id), '-c', '9F', '3'
        ])

        if returncode == 0:
            result['spi_ok'] = True
            result['messages'].append(f"[OK] SPI 读取正常: {output.strip()}")
            print(f"  [OK] 读取芯片 ID: {output.strip()}")
        else:
            result['messages'].append(f"[FAIL] SPI 读取失败: {output}")
            print(f"  [FAIL] {output}")
            return result

        # 3. 测试 SPI 写入
        print("\n[3/3] 测试 SPI 写入...")
        # 使用 spiwrite 发送 0x80 + 4 bytes data (写入配置寄存器 0)
        returncode, output = self.run_command([
            'spiwrite', '-i', str(self.device_id), '80', '00', '00', '00', '00'
        ])

        if returncode == 0:
            result['success'] = True
            result['messages'].append("[OK] SPI 写入正常")
            print("  [OK] SPI 写入测试通过")
        else:
            result['messages'].append(f"[FAIL] SPI 写入失败: {output}")
            print(f"  [FAIL] {output}")

        print("\n" + "=" * 60)
        if result['success']:
            print("[OK] SPI 连接检测通过!")
        else:
            print("[FAIL] SPI 连接检测失败!")
        print("=" * 60)

        return result

    def run_command(self, cmd: List[str]) -> Tuple[int, str]:
        """执行 jtool 命令"""
        full_cmd = [self.jtool] + cmd
        try:
            result = subprocess.run(
                full_cmd,
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode, result.stdout + result.stderr
        except Exception as e:
            return -1, str(e)

    def write_register(self, reg_addr: str, data: List[str]) -> Tuple[int, str]:
        """
        向寄存器写入数据

        TDC-GP22 SPI 协议:
        - 写入 Reg x 的 opcode: 0x8x (x = 0-6)
        - 后跟 4 字节数据 (MSB first)
        - 例: 写入 Reg 0 -> 发送 0x80 + 4 bytes data

        Args:
            reg_addr: 寄存器地址 (如 "00", "01")
            data: 数据字节列表 (如 ["11", "22", "33", "44"])

        Returns:
            (returncode, output)
        """
        # 构造 opcode: 0x80 + 寄存器地址
        # 例如: reg_addr="01" -> opcode="81"
        # 注意: reg_addr 可能是 "00"-"06", 取最后一位
        reg_num = reg_addr[-1]  # 取最后一位数字
        opcode = f"8{reg_num}"
        # 使用 spiwrite 直接发送 opcode + data
        cmd = ['spiwrite', '-i', str(self.device_id), opcode] + data
        return self.run_command(cmd)

    def read_register(self, reg_addr: str, length: int = 4) -> Tuple[int, str]:
        """
        读取寄存器数据

        TDC-GP22 SPI 协议:
        - 读取 Reg x 的 opcode: 0xBx (x = 0-6)
        - 例: 读取 Reg 0 -> 发送 0xB0，然后读取数据

        Args:
            reg_addr: 寄存器地址 ("00"-"06")
            length: 读取字节数

        Returns:
            (returncode, output)
        """
        # 构造读取 opcode: 0xB0 + 寄存器地址
        # 例如: reg_addr="01" -> opcode="B1"
        # 注意: reg_addr 可能是 "00"-"06", 取最后一位
        reg_num = reg_addr[-1]  # 取最后一位数字
        opcode = f"B{reg_num}"
        cmd = ['spircmd', '-i', str(self.device_id), '-c', opcode, str(length)]
        return self.run_command(cmd)

    def configure_alternating_mode(self, pulse_count: int = 20) -> Dict:
        """
        配置交替发波模式 (Measurement Mode 2)

        根据 TDC-GP22 手册配置寄存器:
        - Reg 0: ANZ_FIRE(发波数), DIV_FIRE, MESSB2=1(模式2)
        - Reg 1: HIT1, HIT2, HITIN1, HITIN2
        - Reg 2: DELVAL1(延时), EN_INT
        - Reg 3: EN_FIRST_WAVE, SEL_TIMO_MB2
        - Reg 6: EN_ANALOG=1(使能模拟部分), START_CLKHS, TW2

        Args:
            pulse_count: 发波脉冲数量 (1-127, 默认 20)

        Returns:
            配置结果
        """
        result = {
            'test_name': 'Configure Alternating Mode',
            'success': False,
            'config': {},
        }

        print(f"\n[CONFIG] 配置交替发波模式，脉冲数量: {pulse_count}")

        # 限制脉冲数量范围
        pulse_count = max(1, min(127, pulse_count))

        # --- 配置寄存器 0 (0x80): 基本配置 ---
        # Bit 28-31 (ANZ_FIRE[3:0]): 脉冲数低4位
        # Bit 24-27 (DIV_FIRE): Fire脉冲分频
        # Bit 20-21 (DIV_CLKHS): HS时钟分频
        # Bit 18-19 (START_CLKHS[1:0]): 振荡器稳定时间
        # Bit 17 (ANZ_PORT): 温度端口数
        # Bit 16 (TCYCLE): 温度测量周期
        # Bit 15 (ANZ_FAKE): 虚拟测量数
        # Bit 14 (SEL_ECLK_CMP): 温度时钟选择
        # Bit 13 (CALIBRATE): 校准使能
        # Bit 12 (NO_CAL_AUTO): 自动校准禁用
        # Bit 11 (MESSB2): 测量模式2 (1=模式2)
        # Bit 8-10: NEG_STOP2, NEG_STOP1, NEG_START
        # Bit 0-7 (ID0): ID字节

        # 默认值: 0x22A2C8_00 (手册默认值)
        # 修改 MESSB2=1 (模式2), 设置 ANZ_FIRE
        # Byte 3: ANZ_FIRE[3:0] + DIV_FIRE
        anz_fire_high = (pulse_count >> 3) & 0x0F  # ANZ_FIRE 高位在 Reg 6
        div_fire = 0x02  # 默认分频
        byte3 = (anz_fire_high << 4) | div_fire
        # Byte 2: DIV_CLKHS + START_CLKHS + ANZ_PORT + TCYCLE + ANZ_FAKE + SEL_ECLK_CMP
        byte2 = 0x22  # 默认值部分
        # Byte 1: CALIBRATE + NO_CAL_AUTO + MESSB2 + NEG bits
        byte1 = 0xA8 | 0x08  # MESSB2=1 (模式2)
        # Byte 0: ID0
        byte0 = 0x00

        config_0 = [f"{byte3:02X}", f"{byte2:02X}", f"{byte1:02X}", f"{byte0:02X}"]

        returncode, output = self.write_register(self.REG_CONFIG_0, config_0)
        result['config']['CONFIG_0'] = {'data': config_0, 'raw': ''.join(config_0), 'output': output.strip()}

        if returncode != 0:
            result['error'] = f"配置寄存器 0 失败: {output}"
            return result

        # --- 配置寄存器 1 (0x81): 发波控制和ALU ---
        # Bit 28-31 (HIT2): ALU操作数2
        # Bit 24-27 (HIT1): ALU操作数1
        # Bit 23 (EN_FAST_INIT): 快速初始化
        # Bit 19-21 (HITIN2): Stop2命中数
        # Bit 16-18 (HITIN1): Stop1命中数
        # Bit 15 (CURR32K): 32k振荡器电流
        # Bit 14 (SEL_START_FIRE): Fire作为Start
        # Bit 11-13 (SEL_TST02): EN_START引脚功能
        # Bit 8-10 (SEL_TST01): FIRE_IN引脚功能
        # Bit 0-7 (ID1): ID字节

        # 默认: HIT1=5(no action), HIT2=5(no action), HITIN1=0, HITIN2=0
        hit1 = 0x05  # 默认值
        hit2 = 0x05  # 默认值
        byte3 = (hit2 << 4) | hit1
        byte2 = 0x00
        byte1 = 0x00
        byte0 = 0x00

        config_1 = [f"{byte3:02X}", f"{byte2:02X}", f"{byte1:02X}", f"{byte0:02X}"]

        returncode, output = self.write_register(self.REG_CONFIG_1, config_1)
        result['config']['CONFIG_1'] = {'data': config_1, 'raw': ''.join(config_1), 'output': output.strip()}

        if returncode != 0:
            result['error'] = f"配置寄存器 1 失败: {output}"
            return result

        # --- 配置寄存器 2 (0x82): DELVAL1 和 中断 ---
        # Bit 29-31 (EN_INT[2:0]): 中断使能
        # Bit 27 (RFEDGE2): Stop2边沿
        # Bit 28 (RFEDGE1): Stop1边沿
        # Bit 8-23 (DELVAL1): Stop使能延时值
        # Bit 0-7 (ID2): ID字节

        # EN_INT = 0b001 (ALU中断使能), DELVAL1 = 0 (如果没有模拟部分)
        en_int = 0x01  # ALU中断使能
        delval1_high = 0x00
        byte3 = (en_int << 5) | delval1_high
        byte2 = 0x00  # DELVAL1 中字节
        byte1 = 0x00  # DELVAL1 低字节
        byte0 = 0x00  # ID2

        config_2 = [f"{byte3:02X}", f"{byte2:02X}", f"{byte1:02X}", f"{byte0:02X}"]

        returncode, output = self.write_register(self.REG_CONFIG_2, config_2)
        result['config']['CONFIG_2'] = {'data': config_2, 'raw': ''.join(config_2), 'output': output.strip()}

        if returncode != 0:
            result['error'] = f"配置寄存器 2 失败: {output}"
            return result

        # --- 配置寄存器 3 (0x83): 首波检测和超时 ---
        # Bit 31 (EN_AUTOCALC_MB2): 自动计算
        # Bit 30 (EN_FIRST_WAVE): 首波检测
        # Bit 29 (EN_ERR_VAL): 错误值使能
        # Bit 27-28 (SEL_TIMO_MB2): 超时选择 (3=4096us @ 4MHz)
        # Bit 20-25 (DELREL3): 第3个Stop相对首波
        # Bit 14-19 (DELREL2): 第2个Stop相对首波
        # Bit 8-13 (DELREL1): 第1个Stop相对首波
        # Bit 0-7 (ID3): ID字节

        # 默认配置: 超时=3 (4096us), 不启用首波检测
        sel_timo = 0x03  # 4096us 超时
        en_first_wave = 0
        en_autocalc = 0
        byte3 = (en_autocalc << 7) | (en_first_wave << 6) | (sel_timo << 3)
        byte2 = 0x00
        byte1 = 0x00
        byte0 = 0x00

        config_3 = [f"{byte3:02X}", f"{byte2:02X}", f"{byte1:02X}", f"{byte0:02X}"]

        returncode, output = self.write_register(self.REG_CONFIG_3, config_3)
        result['config']['CONFIG_3'] = {'data': config_3, 'raw': ''.join(config_3), 'output': output.strip()}

        if returncode != 0:
            result['error'] = f"配置寄存器 3 失败: {output}"
            return result

        # --- 配置寄存器 5 (0x85): Fire 脉冲控制 ---
        # Bit 31 (CONF_FIRE[3]): FIRE_BOTH (1=反向FIRE_DOWN)
        # Bit 30 (CONF_FIRE[2]): FIRE_UP 使能 (1=使能)
        # Bit 29 (CONF_FIRE[1]): FIRE_DOWN 使能 (1=使能)
        # Bit 28 (EN_STARTNOISE): Start噪声单元
        # Bit 27 (DIS_PHASESHIFT): 禁用相位噪声
        # Bit 24-26 (REPEAT_FIRE): 脉冲序列重复次数
        # Bit 8-23 (PHFIRE): 各脉冲相位反转配置
        # Bit 0-7 (ID5): ID字节

        # 使能 FIRE_UP 输出 (用于上行测量)
        fire_up_en = 1  # Bit 30
        fire_down_en = 0  # Bit 29，单向测量时禁用
        byte3 = (fire_up_en << 6) | (fire_down_en << 5)
        byte2 = 0x00  # REPEAT_FIRE=0, PHFIRE高字节
        byte1 = 0x00  # PHFIRE低字节
        byte0 = 0x00  # ID5

        config_5 = [f"{byte3:02X}", f"{byte2:02X}", f"{byte1:02X}", f"{byte0:02X}"]

        returncode, output = self.write_register("05", config_5)
        result['config']['CONFIG_5'] = {'data': config_5, 'raw': ''.join(config_5), 'output': output.strip()}

        if returncode != 0:
            result['error'] = f"配置寄存器 5 失败: {output}"
            return result

        # --- 配置寄存器 6 (0x86): 模拟部分控制 ---
        # Bit 31 (EN_ANALOG): 使能模拟部分 (1=使能)
        # Bit 30 (NEG_STOP_TEMP): 温度Stop反相
        # Bit 25-28 (DA_KORR): 比较器偏移校正
        # Bit 22-23 (TW2): 接收电容充电时间 (3=300us)
        # Bit 20 (START_CLKHS[2]): HS振荡器稳定时间高位
        # Bit 18-19 (CYCLE_TOF): TOF测量周期
        # Bit 16-17 (CYCLE_TEMP): 温度测量周期
        # Bit 15 (HZ60): 50/60Hz选择
        # Bit 12 (DOUBLE_RES): 双倍分辨率
        # Bit 13 (QUAD_RES): 四倍分辨率
        # Bit 11 (TEMP_PORTDIR): 温度端口方向
        # Bit 8-10 (ANZ_FIRE[6:4]): 脉冲数高位
        # Bit 0-7 (ID6): ID字节

        # 使能模拟部分, TW2=3 (300us), ANZ_FIRE高位
        en_analog = 1
        tw2 = 0x03  # 300us
        anz_fire_low = pulse_count & 0x07  # ANZ_FIRE[6:4]
        start_clkhs = 0x01  # 480us

        byte3 = (en_analog << 7) | 0x00
        byte2 = (tw2 << 6) | (start_clkhs << 4) | 0x00
        byte1 = 0x00
        byte0 = (anz_fire_low << 4) | 0x00  # ID6 + ANZ_FIRE高位

        config_6 = [f"{byte3:02X}", f"{byte2:02X}", f"{byte1:02X}", f"{byte0:02X}"]

        returncode, output = self.write_register("06", config_6)
        result['config']['CONFIG_6'] = {'data': config_6, 'raw': ''.join(config_6), 'output': output.strip()}

        result['success'] = returncode == 0
        return result

    def send_opcode(self, opcode: str) -> Tuple[int, str]:
        """
        发送单个 opcode 到 TDC-GP22

        Args:
            opcode: 十六进制 opcode (如 "70", "01")

        Returns:
            (returncode, output)
        """
        # 使用 spiwrite 发送单个字节 opcode
        cmd = ['spiwrite', '-i', str(self.device_id), opcode]
        return self.run_command(cmd)

    def init_tdc(self) -> Dict:
        """
        初始化 TDC-GP22 (发送 0x70 opcode)

        Returns:
            初始化结果
        """
        result = {
            'test_name': 'Init TDC',
            'success': False,
        }

        print("\n[INIT] 初始化 TDC-GP22...")

        # 发送 Init opcode (0x70)
        returncode, output = self.send_opcode('70')

        result['output'] = output.strip()
        result['success'] = returncode == 0

        if result['success']:
            print("  [OK] TDC 已初始化")
        else:
            print(f"  [FAIL] 初始化失败: {output}")

        return result

    def start_measurement(self) -> Dict:
        """
        启动单次测量 (发送 0x01 opcode)

        TDC-GP22 测量流程:
        1. 先发送 0x70 (Init) 初始化
        2. 再发送 0x01 (Start_TOF) 启动测量

        Returns:
            启动结果
        """
        result = {
            'test_name': 'Start Measurement',
            'success': False,
        }

        print("\n[MEASURE] 启动测量...")

        # 发送 Start_TOF opcode (0x01)
        returncode, output = self.send_opcode('01')

        result['output'] = output.strip()
        result['success'] = returncode == 0

        if result['success']:
            print("  [OK] 测量已启动")
        else:
            print(f"  [FAIL] 启动失败: {output}")

        return result

    def wait_for_measurement(self, timeout: float = 1.0) -> Dict:
        """
        等待测量完成

        Args:
            timeout: 超时时间（秒）

        Returns:
            等待结果
        """
        result = {
            'test_name': 'Wait for Measurement',
            'success': False,
        }

        print(f"\n[WAIT] 等待测量完成 (超时: {timeout}s)...")

        start_time = time.time()
        while time.time() - start_time < timeout:
            # 读取状态寄存器
            returncode, output = self.read_register(self.REG_STATUS, 1)

            if returncode == 0:
                # 检查状态位 (假设 bit 0 表示测量完成)
                status_val = output.strip().split()
                if status_val and status_val[0] != '00':
                    print(f"  [OK] 测量完成，状态: {output.strip()}")
                    result['success'] = True
                    result['status'] = output.strip()
                    return result

            time.sleep(0.01)  # 10ms 轮询

        result['error'] = '等待测量超时'
        print(f"  [TIMEOUT] 测量未完成")
        return result

    def read_measurement_result(self) -> Dict:
        """
        读取测量结果

        Returns:
            读取结果，包含时间值
        """
        result = {
            'test_name': 'Read Measurement Result',
            'success': False,
            'time_value': None,
        }

        print("\n[READ] 读取测量结果...")

        # 读取结果寄存器 RES_3 (opcode 0xB3) - 测量模式2的自动计算结果
        returncode, output = self.read_register(self.REG_RES_3, 4)

        result['output'] = output.strip()

        if returncode == 0:
            # 解析时间值
            bytes_data = output.strip().split()
            if len(bytes_data) >= 4:
                # 将 4 字节转换为时间值 (大端序)
                time_val = (int(bytes_data[0], 16) << 24 |
                           int(bytes_data[1], 16) << 16 |
                           int(bytes_data[2], 16) << 8 |
                           int(bytes_data[3], 16))
                result['time_value'] = time_val
                result['time_ps'] = time_val * 90  # TDC-GP22 分辨率约 90ps
                result['success'] = True
                print(f"  [OK] 时间值: {time_val} ({time_val * 90} ps)")
            else:
                result['error'] = f"数据长度不足: {bytes_data}"
                print(f"  [FAIL] {result['error']}")
        else:
            result['error'] = output
            print(f"  [FAIL] 读取失败: {output}")

        return result

    def read_temperature(self) -> Dict:
        """
        读取温度测量结果

        Returns:
            温度结果
        """
        result = {
            'test_name': 'Read Temperature',
            'success': False,
            'temperature': None,
        }

        print("\n[TEMP] 读取温度...")

        # 温度测量结果存储在 RES_0 (opcode 0xB0)
        returncode, output = self.read_register(self.REG_RES_0, 4)

        result['output'] = output.strip()

        if returncode == 0:
            bytes_data = output.strip().split()
            if len(bytes_data) >= 4:
                # 解析温度值
                temp_val = (int(bytes_data[0], 16) << 24 |
                           int(bytes_data[1], 16) << 16 |
                           int(bytes_data[2], 16) << 8 |
                           int(bytes_data[3], 16))
                result['temperature_raw'] = temp_val
                result['success'] = True
                print(f"  [OK] 温度原始值: {temp_val}")
            else:
                print(f"  [INFO] 温度数据: {bytes_data}")

        return result

    def run_alternating_measurement(self, pulse_count: int = 20) -> List[Dict]:
        """
        运行完整的交替发波测量流程

        Args:
            pulse_count: 发波脉冲数量

        Returns:
            所有测试结果
        """
        print("=" * 60)
        print(f"TDC-GP22 超声波水表测试")
        print(f"模式: 交替发波，脉冲数量: {pulse_count}")
        print("=" * 60)

        results = []

        # 步骤 1: 配置芯片
        config_result = self.configure_alternating_mode(pulse_count)
        results.append(config_result)

        if not config_result['success']:
            print("\n[ERROR] 配置失败，停止测试")
            return results

        # 步骤 2: 初始化 TDC (发送 0x70)
        init_result = self.init_tdc()
        results.append(init_result)

        if not init_result['success']:
            print("\n[ERROR] 初始化失败，停止测试")
            return results

        # 步骤 3: 启动测量
        start_result = self.start_measurement()
        results.append(start_result)

        if not start_result['success']:
            print("\n[ERROR] 启动测量失败")
            return results

        # 步骤 4: 等待测量完成
        wait_result = self.wait_for_measurement(timeout=2.0)
        results.append(wait_result)

        # 步骤 5: 读取结果
        result_data = self.read_measurement_result()
        results.append(result_data)

        # 步骤 6: 读取温度
        temp_result = self.read_temperature()
        results.append(temp_result)

        return results

    def run_multiple_measurements(self, count: int = 5, pulse_count: int = 20) -> List[Dict]:
        """
        运行多次测量，获取统计数据

        Args:
            count: 测量次数
            pulse_count: 每次测量的脉冲数量

        Returns:
            所有测量结果
        """
        print("=" * 60)
        print(f"TDC-GP22 多次测量测试")
        print(f"次数: {count}, 脉冲: {pulse_count}")
        print("=" * 60)

        all_results = []
        time_values = []

        # 先配置芯片
        config_result = self.configure_alternating_mode(pulse_count)
        if not config_result['success']:
            print("[ERROR] 配置失败")
            return [config_result]

        # 初始化 TDC
        init_result = self.init_tdc()
        if not init_result['success']:
            print("[ERROR] 初始化失败")
            return [config_result, init_result]

        for i in range(count):
            print(f"\n--- 测量 {i+1}/{count} ---")

            # 初始化并启动测量
            self.init_tdc()
            self.start_measurement()

            # 等待
            self.wait_for_measurement(timeout=2.0)

            # 读取结果
            result = self.read_measurement_result()
            all_results.append(result)

            if result['success'] and result['time_value'] is not None:
                time_values.append(result['time_value'])

            # 测量间隔
            time.sleep(0.1)

        # 统计结果
        print("\n" + "=" * 60)
        print("统计结果")
        print("=" * 60)

        if time_values:
            avg_time = sum(time_values) / len(time_values)
            min_time = min(time_values)
            max_time = max(time_values)

            print(f"测量次数: {len(time_values)}")
            print(f"平均时间值: {avg_time}")
            print(f"最小时间值: {min_time}")
            print(f"最大时间值: {max_time}")
            print(f"波动范围: {max_time - min_time}")
        else:
            print("未获取有效时间值")

        return all_results

    def print_report(self, results: List[Dict]):
        """打印测试报告"""
        print("\n" + "=" * 60)
        print("测试报告")
        print("=" * 60)

        for i, r in enumerate(results, 1):
            status = "[PASS]" if r.get('success') else "[FAIL]"
            print(f"\n{i}. {r.get('test_name', 'Unknown')}: {status}")

            if 'time_value' in r and r['time_value'] is not None:
                print(f"   时间值: {r['time_value']} ({r.get('time_ps', 'N/A')} ps)")

            if 'error' in r:
                print(f"   错误: {r['error']}")

        passed = sum(1 for r in results if r.get('success'))
        print(f"\n总计: {passed}/{len(results)} 通过")
        print("=" * 60)


def main():
    """主函数"""
    # 创建测试实例
    tester = TDC_GP22_Ultrasonic(device_id=0)

    # 步骤 0: SPI 连接检测
    spi_check = tester.check_spi_connection()
    if not spi_check['success']:
        print("\n[ERROR] SPI 连接检测失败，停止测试")
        print("请检查:")
        print("  1. JTool-SPI 设备是否连接")
        print("  2. USB 连接是否正常")
        print("  3. 驱动是否正确安装")
        return

    # 运行单次交替发波测量
    print("\n" + "=" * 60)
    print("测试 1: 单次交替发波测量 (20 脉冲)")
    print("=" * 60)
    results = tester.run_alternating_measurement(pulse_count=20)
    tester.print_report(results)

    # 自动进行多次测量统计（跳过交互式输入）
    print("\n" + "=" * 60)
    print("测试 2: 多次测量统计 (3 次)")
    print("=" * 60)
    tester.run_multiple_measurements(count=3, pulse_count=20)

    print("\n测试完成!")


if __name__ == '__main__':
    main()

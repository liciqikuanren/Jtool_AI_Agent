"""
TDC-GP22 双向交替测量流程
功能: 超声波流量计标准测量 - 自动完成上下游测量
生成时间: 2025-03-11

执行流程:
1. 初始化 TDC (0x70)
2. 启动双向测量 (0x05 START_TOF_Restart)
3. 等待第1次中断 (上行测量完成)
4. 读取上行状态和结果
5. 重新初始化 (0x70)
6. 等待第2次中断 (下行测量完成)
7. 读取下行状态和结果
8. 计算流速
"""

import subprocess
import sys
import time
from pathlib import Path
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass
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


@dataclass
class FlowResult:
    """流量测量结果数据结构"""
    tof_up: float = 0.0           # 上行飞行时间 (微秒)
    tof_down: float = 0.0         # 下行飞行时间 (微秒)
    delta_t: float = 0.0          # 时间差 (微秒)
    flow_rate: float = 0.0        # 计算出的流速
    status: int = 0               # 状态标志
    raw_up: int = 0               # 上行原始值
    raw_down: int = 0             # 下行原始值
    timestamp: str = ""

    # 状态标志位
    FLOW_TIMEOUT_UP = 0x01
    FLOW_TIMEOUT_DOWN = 0x02
    FLOW_ERROR_UP = 0x04
    FLOW_ERROR_DOWN = 0x08


class TDC_GP22_Bidirectional:
    """
    TDC-GP22 双向交替测量类

    实现超声波流量计标准测量流程:
    - 自动完成上下游测量
    - 支持首波检测模式
    - 计算流速
    """

    # TDC-GP22 命令
    CMD_INIT = "70"               # 初始化/复位
    CMD_START_TOF = "01"          # 单次测量
    CMD_START_TOF_RESTART = "05"  # 双向交替测量

    # TDC-GP22 寄存器
    REG_STATUS = "B4"             # 状态寄存器
    REG_RESULT = "B3"             # 结果寄存器 (飞行时间)
    REG_RES_3 = "B2"              # 结果3 (平均值)
    REG_PW1ST = "B1"              # 首波脉冲宽度

    def __init__(self, device_id: int = 0):
        self.chip_name = "TDC-GP22"
        self.jtool = get_jtool_path()
        self.device_id = device_id

        # 测量参数
        self.timeout_ms = 10          # 超时时间 (毫秒)
        self.cycle_tof = 1            # 周期系数 (20ms * cycle_tof)

        # TDC 分辨率 (约 90ps = 0.00009 us)
        self.tdc_resolution_ps = 90

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

    def spi_send_byte(self, cmd_byte: str) -> Tuple[int, str]:
        """
        发送单字节命令

        Args:
            cmd_byte: 命令字节 (如 "70", "05")
        """
        return self.run_command([
            'spiwcmd', '-i', str(self.device_id), '-c', cmd_byte
        ])

    def spi_read_result(self, reg_addr: str, length: int = 4) -> Tuple[int, Optional[int], str]:
        """
        读取寄存器结果

        Args:
            reg_addr: 寄存器地址
            length: 读取字节数

        Returns:
            (returncode, value, output)
        """
        returncode, output = self.run_command([
            'spircmd', '-i', str(self.device_id), '-c', reg_addr, str(length)
        ])

        if returncode != 0:
            return returncode, None, output

        # 解析返回数据
        bytes_data = output.strip().split()
        if len(bytes_data) >= length:
            # 将字节组合成整数 (大端序)
            value = 0
            for i in range(length):
                value = (value << 8) | int(bytes_data[i], 16)
            return 0, value, output.strip()

        return -1, None, f"数据长度不足: {bytes_data}"

    def check_interrupt(self) -> bool:
        """
        检查中断状态 (INTN=LOW)

        通过读取状态寄存器判断测量是否完成
        """
        returncode, value, output = self.spi_read_result(self.REG_STATUS, 2)

        if returncode == 0 and value is not None:
            # 检查 INTN 状态 (假设 bit 0 表示中断)
            # 实际应根据硬件连接检测 INTN 引脚
            # 这里简化为状态非零即表示有结果
            return True

        return False

    def wait_for_interrupt(self, timeout_ms: int = 10) -> Tuple[bool, str]:
        """
        等待中断 (测量完成)

        Args:
            timeout_ms: 超时时间 (毫秒)

        Returns:
            (success, message)
        """
        start_time = time.time()
        timeout_sec = timeout_ms / 1000.0

        while time.time() - start_time < timeout_sec:
            # 读取状态寄存器检查测量是否完成
            returncode, value, output = self.spi_read_result(self.REG_STATUS, 2)

            if returncode == 0 and value is not None:
                # 检查是否有错误 (bit 9-10: 超时或错误)
                if value & 0x0600:
                    return False, f"测量错误: 状态=0x{value:04X}"

                # 检查结果有效 (假设 bit 0 表示完成)
                # 简化处理: 如果返回值非零且没有错误位，则认为完成
                if value != 0:
                    return True, f"测量完成: 状态=0x{value:04X}"

            # 短暂延时 (100us 轮询)
            time.sleep(0.0001)

        return False, f"等待超时 ({timeout_ms}ms)"

    def raw_to_time(self, raw_value: int) -> float:
        """
        将原始值转换为时间 (微秒)

        TDC-GP22 分辨率约 90ps
        """
        # raw_value 是 TDC 计数
        # 时间 = 计数 * 分辨率 (ps) / 1000000 = 微秒
        time_us = (raw_value * self.tdc_resolution_ps) / 1000000.0
        return time_us

    def calculate_flow_rate(self, delta_t: float) -> float:
        """
        根据时间差计算流速

        简化公式: v = k * delta_t
        实际应根据管道参数校准

        Args:
            delta_t: 上下游时间差 (微秒)

        Returns:
            流速 (m/s)
        """
        # 简化计算，实际应根据管道直径、声速等参数
        # v = (c^2 * delta_t) / (2 * L * cos(theta))
        # c = 声速 (约 1500 m/s in water)
        # L = 声道长度
        # theta = 声波与流速夹角

        # 这里使用比例系数 k = 0.1 (示例值)
        k = 0.1
        flow_rate = k * delta_t  # m/s
        return flow_rate

    def measure_flow_cycle(self) -> FlowResult:
        """
        执行完整的双向交替测量流程

        标准超声波流量计测量流程:
        1. INIT -> 2. START_TOF_Restart -> 3. 等待上行 -> 4. 读上行结果
        5. INIT -> 6. 等待下行 -> 7. 读下行结果 -> 8. 计算流速
        """
        result = FlowResult()
        result.timestamp = datetime.now().isoformat()

        print("\n" + "=" * 60)
        print("双向交替测量流程")
        print("=" * 60)

        # ========== 步骤1: 初始化 TDC ==========
        print("\n[步骤1] 初始化 TDC (INIT 0x70)...")
        returncode, output = self.spi_send_byte(self.CMD_INIT)
        if returncode != 0:
            result.status |= FlowResult.FLOW_ERROR_UP
            print(f"  [FAIL] 初始化失败: {output}")
            return result
        print("  [OK] 初始化完成")
        time.sleep(0.01)  # 10us 延时

        # ========== 步骤2: 启动双向测量 ==========
        print("\n[步骤2] 启动双向测量 (START_TOF_Restart 0x05)...")
        returncode, output = self.spi_send_byte(self.CMD_START_TOF_RESTART)
        if returncode != 0:
            result.status |= FlowResult.FLOW_ERROR_UP
            print(f"  [FAIL] 启动失败: {output}")
            return result
        print("  [OK] 双向测量已启动")
        print("        -> FIRE_UP 激活 (上行测量)")

        # ========== 步骤3: 等待第1次中断 (上行完成) ==========
        print("\n[步骤3] 等待上行测量完成...")
        success, message = self.wait_for_interrupt(self.timeout_ms)
        if not success:
            result.status |= FlowResult.FLOW_TIMEOUT_UP
            print(f"  [FAIL] {message}")
            # 继续尝试读取结果
        else:
            print(f"  [OK] {message}")

        # ========== 步骤4: 读取上行状态和结果 ==========
        print("\n[步骤4] 读取上行结果...")

        # 读取状态
        returncode, stat_up, output = self.spi_read_result(self.REG_STATUS, 2)
        if returncode == 0:
            print(f"  状态寄存器: 0x{stat_up:04X}")
            if stat_up & 0x0600:
                result.status |= FlowResult.FLOW_ERROR_UP
                print(f"  [WARN] 上行测量错误: 状态=0x{stat_up:04X}")

        # 读取结果
        returncode, raw_up, output = self.spi_read_result(self.REG_RESULT, 4)
        if returncode == 0:
            result.raw_up = raw_up
            result.tof_up = self.raw_to_time(raw_up)
            print(f"  [OK] 上行原始值: {raw_up}")
            print(f"       上行时间: {result.tof_up:.6f} us")
        else:
            result.status |= FlowResult.FLOW_ERROR_UP
            print(f"  [FAIL] 读取上行结果失败: {output}")

        # ========== 步骤5: 重新初始化 (准备读下行) ==========
        print("\n[步骤5] 重新初始化 (准备读下行)...")
        returncode, output = self.spi_send_byte(self.CMD_INIT)
        if returncode != 0:
            result.status |= FlowResult.FLOW_ERROR_DOWN
            print(f"  [FAIL] 初始化失败: {output}")
            return result
        print("  [OK] 初始化完成")
        print("        -> FIRE_DOWN 激活 (下行测量)")

        # 等待周期延时 (50/60Hz 噪声抑制)
        # 默认 CYCLE_TOF=1 时等待 20ms
        cycle_delay = 0.02 * self.cycle_tof
        print(f"  等待周期延时 ({cycle_delay*1000:.0f}ms)...")
        time.sleep(cycle_delay)

        # ========== 步骤6: 等待第2次中断 (下行完成) ==========
        print("\n[步骤6] 等待下行测量完成...")
        success, message = self.wait_for_interrupt(self.timeout_ms)
        if not success:
            result.status |= FlowResult.FLOW_TIMEOUT_DOWN
            print(f"  [FAIL] {message}")
        else:
            print(f"  [OK] {message}")

        # ========== 步骤7: 读取下行状态和结果 ==========
        print("\n[步骤7] 读取下行结果...")

        # 读取状态
        returncode, stat_down, output = self.spi_read_result(self.REG_STATUS, 2)
        if returncode == 0:
            print(f"  状态寄存器: 0x{stat_down:04X}")
            if stat_down & 0x0600:
                result.status |= FlowResult.FLOW_ERROR_DOWN
                print(f"  [WARN] 下行测量错误: 状态=0x{stat_down:04X}")

        # 读取结果
        returncode, raw_down, output = self.spi_read_result(self.REG_RESULT, 4)
        if returncode == 0:
            result.raw_down = raw_down
            result.tof_down = self.raw_to_time(raw_down)
            print(f"  [OK] 下行原始值: {raw_down}")
            print(f"       下行时间: {result.tof_down:.6f} us")
        else:
            result.status |= FlowResult.FLOW_ERROR_DOWN
            print(f"  [FAIL] 读取下行结果失败: {output}")

        # ========== 步骤8: 计算流速 ==========
        print("\n[步骤8] 计算流速...")
        if not (result.status & (FlowResult.FLOW_ERROR_UP | FlowResult.FLOW_ERROR_DOWN)):
            result.delta_t = result.tof_down - result.tof_up
            result.flow_rate = self.calculate_flow_rate(result.delta_t)
            print(f"  [OK] 时间差 (Δt): {result.delta_t:.6f} us")
            print(f"       计算流速: {result.flow_rate:.6f} m/s")
        else:
            print("  [WARN] 由于测量错误，跳过流速计算")

        return result

    def run_multiple_cycles(self, count: int = 5) -> List[FlowResult]:
        """
        运行多次双向测量，获取统计数据

        Args:
            count: 测量周期数

        Returns:
            测量结果列表
        """
        print("\n" + "=" * 60)
        print(f"双向交替测量 - 多次统计")
        print(f"测量次数: {count}")
        print("=" * 60)

        results = []

        for i in range(count):
            print(f"\n{'='*60}")
            print(f"测量周期 {i+1}/{count}")
            print("="*60)

            result = self.measure_flow_cycle()
            results.append(result)

            # 周期间隔
            if i < count - 1:
                time.sleep(0.1)

        return results

    def print_statistics(self, results: List[FlowResult]):
        """打印统计结果"""
        print("\n" + "=" * 60)
        print("统计结果")
        print("=" * 60)

        # 筛选有效结果
        valid_results = [r for r in results if not (r.status & 0x0F)]

        if not valid_results:
            print("没有有效的测量结果")
            return

        # 计算统计值
        tof_up_list = [r.tof_up for r in valid_results]
        tof_down_list = [r.tof_down for r in valid_results]
        delta_t_list = [r.delta_t for r in valid_results]
        flow_list = [r.flow_rate for r in valid_results]

        print(f"\n有效测量次数: {len(valid_results)}/{len(results)}")

        print(f"\n上行飞行时间 (us):")
        print(f"  平均值: {sum(tof_up_list)/len(tof_up_list):.6f}")
        print(f"  最小值: {min(tof_up_list):.6f}")
        print(f"  最大值: {max(tof_up_list):.6f}")

        print(f"\n下行飞行时间 (us):")
        print(f"  平均值: {sum(tof_down_list)/len(tof_down_list):.6f}")
        print(f"  最小值: {min(tof_down_list):.6f}")
        print(f"  最大值: {max(tof_down_list):.6f}")

        print(f"\n时间差 (us):")
        print(f"  平均值: {sum(delta_t_list)/len(delta_t_list):.6f}")
        print(f"  最小值: {min(delta_t_list):.6f}")
        print(f"  最大值: {max(delta_t_list):.6f}")

        print(f"\n流速 (m/s):")
        print(f"  平均值: {sum(flow_list)/len(flow_list):.6f}")
        print(f"  最小值: {min(flow_list):.6f}")
        print(f"  最大值: {max(flow_list):.6f}")


def main():
    """主函数"""
    print("=" * 60)
    print("TDC-GP22 双向交替测量流程")
    print("超声波流量计标准测量")
    print("=" * 60)

    # 创建测量实例
    tdc = TDC_GP22_Bidirectional(device_id=0)

    # 单次测量
    print("\n" + "=" * 60)
    print("单次双向测量")
    print("=" * 60)
    result = tdc.measure_flow_cycle()

    # 显示结果
    print("\n" + "=" * 60)
    print("测量结果")
    print("=" * 60)
    print(f"上行时间: {result.tof_up:.6f} us")
    print(f"下行时间: {result.tof_down:.6f} us")
    print(f"时间差 (Δt): {result.delta_t:.6f} us")
    print(f"流速: {result.flow_rate:.6f} m/s")
    print(f"状态: 0x{result.status:02X}")

    # 多次测量统计
    print("\n" + "=" * 60)
    print("多次测量统计 (5次)")
    print("=" * 60)
    results = tdc.run_multiple_cycles(count=5)
    tdc.print_statistics(results)

    print("\n" + "=" * 60)
    print("测试完成!")
    print("=" * 60)


if __name__ == '__main__':
    main()

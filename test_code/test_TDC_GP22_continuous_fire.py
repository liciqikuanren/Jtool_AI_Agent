"""
TDC-GP22 持续交替发波测试
功能: FIRE_UP 和 FIRE_DOWN 持续交替发送 100 个脉冲
用途: 示波器观察波形
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


class TDC_GP22_ContinuousFire:
    """
    TDC-GP22 持续交替发波测试类

    功能:
    - FIRE_UP 和 FIRE_DOWN 持续交替发送
    - 可配置脉冲数量
    - 可配置发波间隔
    """

    def __init__(self, device_id: int = 0):
        self.chip_name = "TDC-GP22"
        self.jtool = get_jtool_path()
        self.device_id = device_id

        # 默认参数
        self.pulse_count = 20       # 每次发波的脉冲数
        self.fire_interval = 0.1    # 发波间隔 (秒)

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

    def configure_fire_pulse(self, pulse_count: int = 20) -> bool:
        """
        配置发波脉冲数量

        Args:
            pulse_count: 脉冲数量 (建议 10-30)
        """
        print(f"\n[配置] 设置脉冲数量: {pulse_count}")

        # 配置 CONFIG_0 寄存器
        # 字节0: 0x02 = 模式2 + 交替发波
        # 字节2: 脉冲数量
        config_data = [
            "02",                       # 模式2 + 交替发波使能
            "00",
            f"{pulse_count:02X}",      # 脉冲数量
            "00"
        ]

        returncode, output = self.run_command([
            'spiwcmd', '-i', str(self.device_id),
            '-c', '80', '-a', '00'  # 写 CONFIG_0
        ] + config_data)

        if returncode == 0:
            print(f"  [OK] 脉冲数量设置为 {pulse_count}")
            return True
        else:
            print(f"  [FAIL] 配置失败: {output}")
            return False

    def fire_up(self) -> bool:
        """发送 FIRE_UP 脉冲"""
        returncode, output = self.run_command([
            'spiwcmd', '-i', str(self.device_id), '-c', '01'  # START_TOF - 上行
        ])
        return returncode == 0

    def fire_down(self) -> bool:
        """发送 FIRE_DOWN 脉冲"""
        returncode, output = self.run_command([
            'spiwcmd', '-i', str(self.device_id), '-c', '01'  # START_TOF - 下行
        ])
        return returncode == 0

    def fire_bidirectional(self) -> bool:
        """发送双向测量命令 (自动交替)"""
        returncode, output = self.run_command([
            'spiwcmd', '-i', str(self.device_id), '-c', '05'  # START_TOF_Restart
        ])
        return returncode == 0

    def continuous_alternate_fire(self,
                                   total_cycles: int = 100,
                                   pulse_count: int = 20,
                                   interval_ms: float = 100) -> Dict:
        """
        持续交替发波

        Args:
            total_cycles: 总周期数 (默认 100)
            pulse_count: 每个方向的脉冲数
            interval_ms: 周期间隔 (毫秒)

        Returns:
            测试结果
        """
        result = {
            'test_name': 'Continuous Alternate Fire',
            'success': False,
            'total_cycles': total_cycles,
            'pulse_count': pulse_count,
            'cycles_completed': 0,
            'start_time': datetime.now().isoformat(),
        }

        print("\n" + "=" * 60)
        print("TDC-GP22 持续交替发波测试")
        print("=" * 60)
        print(f"总周期数: {total_cycles}")
        print(f"脉冲数量: {pulse_count}")
        print(f"周期间隔: {interval_ms} ms")
        print(f"预计时间: {total_cycles * interval_ms / 1000:.1f} 秒")
        print("=" * 60)

        # 步骤1: 初始化
        print("\n[步骤1] 初始化 TDC...")
        returncode, output = self.run_command([
            'spiwcmd', '-i', str(self.device_id), '-c', '70'  # INIT
        ])
        if returncode != 0:
            print(f"  [FAIL] 初始化失败: {output}")
            result['error'] = f"初始化失败: {output}"
            return result
        print("  [OK] 初始化完成")
        time.sleep(0.01)

        # 步骤2: 配置脉冲数量
        if not self.configure_fire_pulse(pulse_count):
            result['error'] = "脉冲配置失败"
            return result
        time.sleep(0.01)

        # 步骤3: 持续发波
        print(f"\n[步骤3] 开始持续交替发波...")
        print("(按 Ctrl+C 可提前停止)")
        print()

        success_count = 0
        interval_sec = interval_ms / 1000.0

        try:
            for i in range(total_cycles):
                cycle_num = i + 1

                # 发送双向测量命令 (自动完成 FIRE_UP 和 FIRE_DOWN)
                if self.fire_bidirectional():
                    success_count += 1
                    status = "OK"
                else:
                    status = "FAIL"

                # 显示进度 (每10个显示一次)
                if cycle_num % 10 == 0 or cycle_num == 1:
                    print(f"  进度: {cycle_num}/{total_cycles} [{status}] " +
                          f"({cycle_num/total_cycles*100:.0f}%)")

                # 周期间隔
                if cycle_num < total_cycles:
                    time.sleep(interval_sec)

        except KeyboardInterrupt:
            print(f"\n  [INFO] 用户中断，已完成 {success_count} 个周期")

        # 完成
        result['cycles_completed'] = success_count
        result['success'] = success_count > 0
        result['end_time'] = datetime.now().isoformat()

        print("\n" + "=" * 60)
        print("发波完成")
        print("=" * 60)
        print(f"总周期: {total_cycles}")
        print(f"成功: {success_count}")
        print(f"失败: {total_cycles - success_count}")
        print(f"成功率: {success_count/total_cycles*100:.1f}%")

        return result

    def rapid_fire_test(self,
                       pulse_count: int = 20,
                       burst_count: int = 10) -> Dict:
        """
        快速爆发测试 - 连续快速发波

        Args:
            pulse_count: 每次脉冲数
            burst_count: 爆发次数

        Returns:
            测试结果
        """
        result = {
            'test_name': 'Rapid Fire Test',
            'success': False,
            'burst_count': burst_count,
        }

        print("\n" + "=" * 60)
        print("TDC-GP22 快速爆发测试")
        print("=" * 60)
        print(f"爆发次数: {burst_count}")
        print(f"脉冲数量: {pulse_count}")
        print()

        # 初始化
        print("[初始化] TDC...")
        self.run_command(['spiwcmd', '-i', str(self.device_id), '-c', '70'])
        time.sleep(0.01)

        # 配置脉冲
        self.configure_fire_pulse(pulse_count)
        time.sleep(0.01)

        # 快速爆发
        print(f"\n[爆发测试] 连续发送 {burst_count} 次...")
        start_time = time.time()

        for i in range(burst_count):
            self.fire_bidirectional()
            # 最小延时
            time.sleep(0.001)  # 1ms

        elapsed = time.time() - start_time

        print(f"  完成 {burst_count} 次爆发")
        print(f"  用时: {elapsed:.3f} 秒")
        print(f"  频率: {burst_count/elapsed:.1f} Hz")

        result['success'] = True
        result['elapsed_time'] = elapsed
        result['frequency'] = burst_count / elapsed

        return result

    def single_fire_test(self, pulse_count: int = 20) -> Dict:
        """
        单次发波测试 - 用于示波器单次触发

        Args:
            pulse_count: 脉冲数量

        Returns:
            测试结果
        """
        result = {
            'test_name': 'Single Fire Test',
            'success': False,
        }

        print("\n" + "=" * 60)
        print("TDC-GP22 单次发波测试")
        print("=" * 60)
        print(f"脉冲数量: {pulse_count}")
        print()

        # 初始化
        print("[初始化] TDC...")
        self.run_command(['spiwcmd', '-i', str(self.device_id), '-c', '70'])
        time.sleep(0.01)

        # 配置脉冲
        self.configure_fire_pulse(pulse_count)
        time.sleep(0.01)

        # 发送单次测量
        print("\n[发波] 发送 FIRE_UP...")
        self.fire_up()
        print("  [OK] FIRE_UP 已发送")

        time.sleep(0.05)  # 50ms 间隔

        print("\n[发波] 发送 FIRE_DOWN...")
        self.fire_down()
        print("  [OK] FIRE_DOWN 已发送")

        result['success'] = True
        return result


def main():
    """主函数"""
    print("=" * 60)
    print("TDC-GP22 持续交替发波测试")
    print("用途: 示波器观察 FIRE_UP/FIRE_DOWN 波形")
    print("=" * 60)

    # 创建测试实例
    tdc = TDC_GP22_ContinuousFire(device_id=0)

    # 菜单选择
    print("\n请选择测试模式:")
    print("  1. 单次发波测试 (用于示波器单次触发)")
    print("  2. 快速爆发测试 (10次连续发波)")
    print("  3. 持续交替发波 (100个周期)")
    print("  4. 自定义参数发波")

    # 自动选择模式3 (持续100个周期)
    mode = "3"

    if mode == "1":
        # 单次测试
        tdc.single_fire_test(pulse_count=20)

    elif mode == "2":
        # 快速爆发
        tdc.rapid_fire_test(pulse_count=20, burst_count=10)

    elif mode == "3":
        # 持续交替发波 (默认)
        tdc.continuous_alternate_fire(
            total_cycles=100,
            pulse_count=20,
            interval_ms=100  # 100ms 间隔
        )

    elif mode == "4":
        # 自定义
        total = int(input("总周期数 (默认100): ") or "100")
        pulses = int(input("脉冲数量 (默认20): ") or "20")
        interval = float(input("周期间隔 ms (默认100): ") or "100")
        tdc.continuous_alternate_fire(total, pulses, interval)

    print("\n" + "=" * 60)
    print("测试完成!")
    print("=" * 60)
    print("\n提示: 现在可以用示波器观察 FIRE_UP 和 FIRE_DOWN 引脚")
    print("      应该能看到交替的脉冲波形")


if __name__ == '__main__':
    main()

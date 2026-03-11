"""
TDC-GP22 Fire 脉冲输出测试
用于验证 Fire 引脚是否正常工作
"""

import subprocess
import time

JTOOL = r'F:\Jooiee\Jtool_AI_Agent\.claude\skills\jtool\scripts\lib\jtool.exe'

def run_cmd(args):
    cmd = [JTOOL] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode, result.stdout + result.stderr

print("=" * 60)
print("TDC-GP22 Fire 脉冲测试")
print("=" * 60)
print()
print("此测试将配置 TDC 并触发 Fire 脉冲输出")
print("请用示波器测量 FIRE_UP 引脚 (Pin 22)")
print()
print("3秒后开始...")
time.sleep(3)

print()
print("[1/5] 配置 Reg 0: 20个脉冲...")
ret, out = run_cmd(['spiwrite', '-i', '0', '80', '22', '22', 'C8', '00'])
print(f"    返回: {'OK' if ret == 0 else 'FAIL'} {out}")

print("[2/5] 配置 Reg 5: 使能 FIRE_UP...")
ret, out = run_cmd(['spiwrite', '-i', '0', '85', '40', '00', '00', '00'])
print(f"    返回: {'OK' if ret == 0 else 'FAIL'} {out}")

print("[3/5] 配置 Reg 6: 使能模拟部分...")
ret, out = run_cmd(['spiwrite', '-i', '0', '86', '80', '60', '00', '00'])
print(f"    返回: {'OK' if ret == 0 else 'FAIL'} {out}")

print("[4/5] 发送 Init (0x70)...")
ret, out = run_cmd(['spiwrite', '-i', '0', '70'])
print(f"    返回: {'OK' if ret == 0 else 'FAIL'} {out}")

time.sleep(0.1)

print("[5/5] 发送 Start_TOF (0x01) - Fire 脉冲输出!...")
ret, out = run_cmd(['spiwrite', '-i', '0', '01'])
print(f"    返回: {'OK' if ret == 0 else 'FAIL'} {out}")

print()
print("=" * 60)
print("Fire 脉冲应该已经输出!")
print("=" * 60)
print()
print("预期波形:")
print("  - 脉冲数: 20 个")
print("  - 频率: 4 MHz (周期 250ns)")
print("  - 幅度: 3.3V CMOS")
print("  - 位置: FIRE_UP 引脚 (Pin 22)")
print()
print("如果看不到波形，请检查:")
print("  1. 示波器探头是否接好 (Pin 22 vs GND)")
print("  2. 示波器触发设置 (上升沿, 1.5V)")
print("  3. 时间基准 (2us/div)")
print()

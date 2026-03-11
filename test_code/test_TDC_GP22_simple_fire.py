"""
TDC-GP22 简化发波测试
直接发送命令，不考虑配置寄存器
"""

import subprocess
import time

import os

# 自动查找 jtool
possible_paths = [
    ".claude/skills/jtool/scripts/lib/jtool.exe",
    "../.claude/skills/jtool/scripts/lib/jtool.exe",
]
JTOOL = None
for p in possible_paths:
    if os.path.exists(p):
        JTOOL = p
        break
if not JTOOL:
    JTOOL = "jtool"  # 使用系统 PATH 中的

def run(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
    return result.returncode, result.stdout + result.stderr

print("="*60)
print("TDC-GP22 简化发波测试")
print("="*60)

# 方法1: 直接发送 0x01 (START_TOF)
print("\n方法1: 发送 START_TOF (0x01)")
print("命令: jtool spiwcmd -i 0 -c 01")
ret, out = run([JTOOL, "spiwcmd", "-i", "0", "-c", "01"])
print(f"结果: {'成功' if ret == 0 else '失败'}")
print(f"输出: {out[:100] if out else '无'}")
time.sleep(0.5)

# 方法2: 发送 INIT + START_TOF
print("\n方法2: INIT + START_TOF")
print("命令: jtool spiwcmd -i 0 -c 70")
run([JTOOL, "spiwcmd", "-i", "0", "-c", "70"])
time.sleep(0.01)

print("命令: jtool spiwcmd -i 0 -c 01")
ret, out = run([JTOOL, "spiwcmd", "-i", "0", "-c", "01"])
print(f"结果: {'成功' if ret == 0 else '失败'}")
time.sleep(0.5)

# 方法3: 双向测量
print("\n方法3: 双向测量 (0x05)")
print("命令: jtool spiwcmd -i 0 -c 70")
run([JTOOL, "spiwcmd", "-i", "0", "-c", "70"])
time.sleep(0.01)

print("命令: jtool spiwcmd -i 0 -c 05")
ret, out = run([JTOOL, "spiwcmd", "-i", "0", "-c", "05"])
print(f"结果: {'成功' if ret == 0 else '失败'}")

print("\n" + "="*60)
print("测试完成")
print("="*60)
print("\n请用示波器检查 FIRE_UP 和 FIRE_DOWN 引脚")
print("正常应该能看到脉冲波形")

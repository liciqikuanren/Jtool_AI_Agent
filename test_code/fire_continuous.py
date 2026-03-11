"""
TDC-GP22 持续交替发波
直接发送命令，不配置寄存器
"""

import subprocess
import time

JTOOL = r".claude\skills\jtool\scripts\lib\jtool.exe"

def fire(cmd):
    """发送命令"""
    subprocess.run(
        [JTOOL, "spiwcmd", "-i", "0", "-c", cmd, "00"],
        capture_output=True, timeout=5
    )

print("="*60)
print("TDC-GP22 持续交替发波")
print("命令: 0x01 (START_TOF) + 数据 0x00")
print("="*60)
print()

# 100个周期
for i in range(100):
    print(f"\r周期: {i+1}/100", end="", flush=True)

    # FIRE_UP
    fire("01")
    time.sleep(0.05)  # 50ms

    # FIRE_DOWN
    fire("01")
    time.sleep(0.05)  # 50ms

print()
print()
print("="*60)
print("发波完成!")
print("请用示波器观察 FIRE_UP 和 FIRE_DOWN 引脚")
print("="*60)

"""
TDC-GP22 直接发波测试 - 16进制命令
功能: 直接发送16进制命令配置脉冲并触发FIRE
生成时间: 2025-03-11
"""

import subprocess
import sys
import time
from pathlib import Path


def get_jtool_path() -> str:
    """获取 jtool 可执行文件路径"""
    possible_paths = [
        Path(__file__).parent.parent / ".claude" / "skills" / "jtool" / "scripts" / "lib" / "jtool.exe",
        Path(".claude/skills/jtool/scripts/lib/jtool.exe"),
        "jtool.exe",
    ]
    for path in possible_paths:
        if isinstance(path, Path) and path.exists():
            return str(path)
    return "jtool"


JTOOL = get_jtool_path()
DEVICE_ID = "0"


def spi_write(cmd_hex: str, addr_hex: str = None, data_hex_list: list = None) -> tuple:
    """
    SPI 写操作

    Args:
        cmd_hex: 命令字节 (如 "80")
        addr_hex: 地址字节 (如 "00")
        data_hex_list: 数据字节列表 (如 ["14", "00", "00", "00"])
    """
    cmd = [JTOOL, 'spiwcmd', '-i', DEVICE_ID, '-c', cmd_hex]

    if addr_hex:
        cmd.extend(['-a', addr_hex])

    if data_hex_list:
        cmd.extend(data_hex_list)

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        return result.returncode, result.stdout + result.stderr
    except Exception as e:
        return -1, str(e)


def spi_read(cmd_hex: str, length: int) -> tuple:
    """
    SPI 读操作

    Args:
        cmd_hex: 命令字节 (如 "B3")
        length: 读取字节数
    """
    cmd = [JTOOL, 'spircmd', '-i', DEVICE_ID, '-c', cmd_hex, str(length)]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        return result.returncode, result.stdout + result.stderr
    except Exception as e:
        return -1, str(e)


def init_tdc():
    """初始化 TDC"""
    print("\n[1] 初始化 TDC (发送 0x70)...")
    ret, out = spi_write("70")
    if ret == 0:
        print("    [OK] 初始化完成")
    else:
        print(f"    [FAIL] {out}")
    time.sleep(0.01)
    return ret == 0


def configure_pulse_count(pulse_count: int = 20):
    """
    配置脉冲数量

    CONFIG_0 寄存器 (地址 0x00):
    - Byte 0: 测量模式 + 交替发波使能
    - Byte 1: 保留
    - Byte 2: 脉冲数量 (如 0x14 = 20)
    - Byte 3: 保留
    """
    print(f"\n[2] 配置脉冲数量: {pulse_count}")

    # 构造 CONFIG_0 数据
    # Byte 0: 0x02 = 模式2 + 交替发波
    # Byte 1: 0x00
    # Byte 2: 脉冲数量
    # Byte 3: 0x00
    pulse_hex = f"{pulse_count:02X}"
    data = ["02", "00", pulse_hex, "00"]

    print(f"    写入 CONFIG_0 (0x00): {' '.join(data)}")

    # 写寄存器: 命令 0x80, 地址 0x00, 数据...
    ret, out = spi_write("80", "00", data)
    if ret == 0:
        print("    [OK] 配置写入完成")
    else:
        print(f"    [FAIL] {out}")

    # 验证写入
    time.sleep(0.01)
    ret, out = spi_read("00", 4)
    print(f"    读取 CONFIG_0: {out.strip()}")

    return ret == 0


def fire_up():
    """发送 FIRE_UP (上行测量)"""
    print("\n[3] 发送 FIRE_UP (命令 0x01)...")
    ret, out = spi_write("01")
    if ret == 0:
        print("    [OK] FIRE_UP 已发送")
    else:
        print(f"    [FAIL] {out}")
    return ret == 0


def fire_down():
    """发送 FIRE_DOWN (下行测量)"""
    print("\n[4] 发送 FIRE_DOWN (命令 0x01 再次)...")
    ret, out = spi_write("01")
    if ret == 0:
        print("    [OK] FIRE_DOWN 已发送")
    else:
        print(f"    [FAIL] {out}")
    return ret == 0


def fire_bidirectional():
    """发送双向测量命令 (自动交替)"""
    print("\n[5] 发送双向测量命令 (0x05)...")
    ret, out = spi_write("05")
    if ret == 0:
        print("    [OK] 双向测量命令已发送")
        print("        -> 自动执行 FIRE_UP 然后 FIRE_DOWN")
    else:
        print(f"    [FAIL] {out}")
    return ret == 0


def continuous_fire(cycles: int = 100, pulse_count: int = 20, interval_ms: int = 100):
    """
    持续交替发波

    Args:
        cycles: 总周期数
        pulse_count: 脉冲数量
        interval_ms: 周期间隔(毫秒)
    """
    print("\n" + "=" * 60)
    print("TDC-GP22 持续交替发波测试 (16进制命令)")
    print("=" * 60)
    print(f"总周期: {cycles}")
    print(f"脉冲数: {pulse_count}")
    print(f"间隔: {interval_ms} ms")
    print(f"预计时间: {cycles * interval_ms / 1000:.1f} 秒")
    print("=" * 60)

    # 初始化
    if not init_tdc():
        print("[ERROR] 初始化失败")
        return

    # 配置脉冲
    if not configure_pulse_count(pulse_count):
        print("[ERROR] 脉冲配置失败")
        return

    # 持续发波
    print("\n[6] 开始持续发波...")
    print("(按 Ctrl+C 停止)\n")

    interval_sec = interval_ms / 1000.0
    success = 0

    try:
        for i in range(cycles):
            cycle = i + 1

            # 发送双向测量命令
            ret, out = spi_write("05")
            if ret == 0:
                success += 1
                status = "OK"
            else:
                status = "FAIL"

            # 显示进度
            if cycle % 10 == 0 or cycle == 1:
                print(f"  进度: {cycle}/{cycles} [{status}] ({cycle/cycles*100:.0f}%)")

            # 间隔
            if cycle < cycles:
                time.sleep(interval_sec)

    except KeyboardInterrupt:
        print(f"\n  [INFO] 用户中断，已完成 {success} 个周期")

    # 完成报告
    print("\n" + "=" * 60)
    print("发波完成")
    print("=" * 60)
    print(f"总周期: {cycles}")
    print(f"成功: {success}")
    print(f"失败: {cycles - success}")
    print(f"成功率: {success/cycles*100:.1f}%")
    print("\n[提示] 现在可以用示波器观察 FIRE_UP 和 FIRE_DOWN 引脚")
    print("       应该能看到 20 个脉冲的波形")


def test_single_fire():
    """单次发波测试 - 用于调试"""
    print("\n" + "=" * 60)
    print("单次发波测试")
    print("=" * 60)

    # 初始化
    init_tdc()

    # 配置 20 个脉冲
    configure_pulse_count(20)

    # 发送 FIRE_UP
    print("\n发送 FIRE_UP...")
    fire_up()

    time.sleep(0.5)

    # 重新初始化
    init_tdc()

    # 发送 FIRE_DOWN
    print("\n发送 FIRE_DOWN...")
    fire_down()

    print("\n[完成] 检查示波器是否有波形")


def main():
    """主函数"""
    import sys

    # 默认执行持续发波
    if len(sys.argv) > 1 and sys.argv[1] == "single":
        test_single_fire()
    else:
        continuous_fire(cycles=100, pulse_count=20, interval_ms=100)


if __name__ == '__main__':
    main()

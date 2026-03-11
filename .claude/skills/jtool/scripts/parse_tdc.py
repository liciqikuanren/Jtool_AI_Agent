import PyPDF2
import re

with open('datasheet/TDC_GP22.pdf', 'rb') as f:
    reader = PyPDF2.PdfReader(f)
    text = ''
    for i, page in enumerate(reader.pages[:15]):
        page_text = page.extract_text()
        if page_text:
            text += page_text + '\n'

# 提取关键信息
print("=" * 60)
print("TDC-GP22 Datasheet Analysis")
print("=" * 60)

# 查找 I2C/SPI 相关信息
if 'SPI' in text:
    print("Interface: SPI")
if 'I2C' in text or 'i2c' in text.lower():
    print("Interface: I2C")

# 查找寄存器地址
reg_matches = re.findall(r'(0x[0-9A-Fa-f]{2,4})', text)
unique_regs = list(set(reg_matches))[:20]
print(f"\nRegister Addresses Found: {len(unique_regs)}")
for r in unique_regs[:10]:
    print(f"  - {r}")

# 查找功能描述
features = []
if 'ultrasonic' in text.lower():
    features.append("Ultrasonic flow measurement")
if 'time' in text.lower() and 'digital' in text.lower():
    features.append("Time-to-Digital Converter")
if 'temperature' in text.lower():
    features.append("Temperature measurement")

print(f"\nFeatures:")
for f in features:
    print(f"  - {f}")

# 查找电压信息
voltage_matches = re.findall(r'(\d+\.?\d*)\s*[Vv]', text)
voltages = []
for v in voltage_matches:
    try:
        val = float(v)
        if 1.0 <= val <= 5.5:
            voltages.append(f"{val}V")
    except:
        pass

print(f"\nVoltage: {', '.join(list(set(voltages))[:3])}")

print("\n" + "=" * 60)
print("Raw text (first 3000 chars):")
print("=" * 60)
print(text[:3000])

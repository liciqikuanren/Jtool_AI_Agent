# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a hardware testing automation project for the JTool USB adapter (www.jooiee.com). JTool is a multi-protocol USB adapter that supports I2C, SPI, GPIO, and CAN bus communication for chip/module testing.

## Project Structure

```
.claude/skills/jtool/
├── jtool.yaml              # Skill definition
├── SKILL.md                # Skill documentation
├── assets/
│   └── datasheet/          # Datasheets for chips/modules (PDF, txt, etc.)
└── scripts/
    ├── lib/
    │   ├── jtool.dll       # JTool device driver library (Windows)
    │   ├── jtool.exe       # JTool command-line executable
    │   └── jtool.h         # C header file with API definitions
    └── src/
        ├── __init__.py            # Package initialization
        ├── jtool.py               # JTool DLL wrapper (ctypes)
        ├── test_framework.py      # Test framework and plan generator
        ├── jtool_skills.py        # Interactive test tool
        ├── scan_devices.py        # Device scanning utility
        ├── README.md              # Source code documentation
        └── examples/
            ├── test_eeprom_at24c02.py  # AT24C02 EEPROM test example
            └── test_flash_w25q.py      # W25Q Flash test example

jtool_skill.py             # Main CLI entry point (root level)
docs/
  需求.md                  # Requirements document (Chinese)
```

## Common Commands

```bash
# Interactive test mode (main entry)
python jtool_skill.py

# Or using the skill system
/skills jtool

# Quick device scan
python jtool_skill.py scan

# Quick I2C test
python jtool_skill.py quick

# Run specific chip tests
python jtool_skill.py test-eeprom --addr 0x50
python jtool_skill.py test-flash

# Direct module execution
python -m .claude.skills.jtool.scripts.src.examples.test_eeprom_at24c02
```

## Architecture

### Layered Structure

1. **DLL Layer** (`.claude/skills/jtool/scripts/src/jtool.py`): ctypes wrapper around `.claude/skills/jtool/scripts/lib/jtool.dll`
   - Device management: `devices_scan()`, `dev_open()`, `dev_close()`
   - Protocol classes: `I2CDevice`, `SPIDevice`, `GPIODevice`
   - Error handling via `JToolError` exceptions

2. **Framework Layer** (`.claude/skills/jtool/scripts/src/test_framework.py`): Test abstraction
   - `TestPlanGenerator`: Creates test cases from chip templates (`CHIP_TEMPLATES`)
   - `TestExecutor`: Executes test cases, manages device lifecycle
   - `DatasheetManager`: Handles `.claude/skills/jtool/assets/datasheet/` directory
   - `TestReporter`: Console and JSON report output

3. **Application Layer**: User-facing tools
   - `jtool_skill.py`: CLI entry with subcommands (at repository root)
   - `.claude/skills/jtool/scripts/src/jtool_skills.py`: Interactive 6-step wizard (`JToolSkills` class)
   - `.claude/skills/jtool/scripts/src/scan_devices.py`: Device discovery utility

### Test Case Structure

Tests are defined as `TestCase` dataclasses with:
- `setup_steps`: List of actions before test
- `test_steps`: List of actions to verify
- `cleanup_steps`: Optional cleanup actions
- `expected_result`: String description of success criteria

Actions are dictionaries like `{"action": "i2c_write", "addr": 0x50, ...}` executed by `TestExecutor._execute_step()`.

### Interactive Workflow

The `JToolSkills` class implements a 6-step workflow:
1. **Select module type** (EEPROM/sensor/Flash/etc.)
2. **Check datasheet** (prompts user to place in `assets/datasheet/`)
3. **Select interface** (I2C/SPI/GPIO/CAN)
4. **Select test functions** (from chip-specific templates)
5. **Configure device** (address, SPI mode, etc.)
6. **Generate and execute** test plan

## Python API Usage

```python
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(".claude/skills/jtool/scripts/src")))

from jtool import open_i2c_device, RegAddrType, dev_close

# Open I2C device
handle, i2c = open_i2c_device()

# Scan bus
count, addresses = i2c.scan()

# Write/Read
i2c.write(0x50, RegAddrType.BIT8, 0x00, b'\xAA\xBB')
data = i2c.read(0x50, RegAddrType.BIT8, 0x00, 2)

# Close
dev_close(handle)
```

## JTool API Reference

### Device Management
- `DevicesScan()` - Scan for connected JTool devices
- `DevOpen()` / `DevClose()` - Open/close device handles

### I2C Operations (`dev_i2c`)
- `I2CScan()` - Scan I2C bus for devices
- `I2CWrite()` / `I2CRead()` - Standard I2C read/write
- `EEWrite()` / `EERead()` - EEPROM operations with page handling
- `I2CRegisterIntCallback()` - Interrupt callbacks

### SPI Operations (`dev_spi`)
- `SPIWriteOnly()` / `SPIReadOnly()` / `SPIWriteRead()` - SPI transfers
- `QSPIWriteOnly()` / `QSPIReadOnly()` - Quad SPI transfers
- `SPIWriteWithCMD()` / `SPIReadWithCMD()` - SPI with command/address fields
- `SPIRegisterIntCallback()` - Interrupt callbacks

### GPIO Operations (`dev_io`)
- `IOSetIn()` / `IOSetOut()` - Configure pin direction
- `IOSetVal()` / `IOGetInVal()` - Read/write digital values
- `PWMSetFreq()` / `PWMSetDuty()` - PWM output
- `ADCSetIn()` / `ADCGetVal()` - ADC input
- `CapSetIn()` / `CapGetVal()` - Capture input (frequency/duty)
- `IOPulseOn()` / `IOPulseCnt()` - Pulse generation

### Error Codes
- `ErrNone` = 0, `ErrParam` = 1, `ErrDisconnect` = 2, `ErrBusy` = 4
- `ErrWaiting` = 8, `ErrTimeOut` = 16, `ErrDataParse` = 32, `ErrFailACK` = 64

## Development Notes

- **Platform**: Windows only (x86-64 DLL)
- **Python Version**: Python 3.7+ recommended
- **Dependencies**: Only standard library (ctypes for DLL access)
- **DLL Loading**: Auto-detects DLL path at `.claude/skills/jtool/scripts/lib/jtool.dll`

### Adding New Chip Support

1. Create test script in `.claude/skills/jtool/scripts/src/examples/test_<chip>.py`
2. Add chip template to `TestPlanGenerator.CHIP_TEMPLATES` in `test_framework.py`
3. Implement `_create_<type>_test_case()` method for custom test logic

### Datasheet Handling

- Place PDF/TXT datasheets in `.claude/skills/jtool/assets/datasheet/` directory
- `DatasheetManager` scans and lists available datasheets
- Interactive tool prompts user to select datasheet when available

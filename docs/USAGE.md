LabJack T7-Pro TDAC Controller — Usage, Install & Test Guide

Overview
--------
This document explains how to install prerequisites, configure the project, run dry-run tests (safe, no hardware writes), and perform the first hardware tests with a LabJack T7-Pro + 11×LJTick-DAC. It also documents CLI usage, profile formats, logging, register mapping, and troubleshooting.

Files added by the skeleton
- docs/SRS.md — Software Requirements Specification
- docs/SDD.md — Software Design Document
- docs/USAGE.md — (this file)
- src/ — Python project skeleton
  - set_tdac.py (CLI & scheduler skeleton)
  - tdac_manager.py (hardware abstraction; supports register_map and LJM calls)
  - waveforms.py, channel.py, profile_loader.py, logger.py, config.py

Prerequisites
-------------
- Windows (targeted platform for V&V testing). The code is Python 3.x compatible.
- Python 3.8+ recommended, installed and on PATH.
- LabJack LJM runtime/library (official LabJack installer) — required for real hardware access. See LabJack docs: https://labjack.com/support/software
- Python wrapper package: labjack-ljm (pip package), which uses the installed LJM runtime.

Install steps (high level)
1. Ensure Python 3 is installed. Use the official installer for Windows and enable "Add Python to PATH".
2. (Optional but recommended) Create a virtual environment in the project root:
   - python -m venv .venv
   - .\.venv\Scripts\activate
3. Install Python dependencies (minimal):
   - pip install --upgrade pip
   - pip install labjack-ljm

4. Install the LabJack LJM runtime (Windows):
   - Download and run the LJM installer from LabJack: https://labjack.com/support/software
   - Follow the LabJack instructions and reboot if required.

Verify LJM is available to Python
--------------------------------
Run a quick Python snippet to verify the library and list device info. Execute in a terminal (within virtualenv if used):

python - <<'PY'
import labjack.ljm as ljm
print('labjack.ljm imported OK')
# Open first T7 found on USB (no serial specified)
try:
    handle = ljm.openS('T7','USB','')
    info = ljm.getHandleInfo(handle)
    print('Device opened:', info)
    ljm.close(handle)
except Exception as e:
    print('Device open/read failed:', e)
PY

If this prints the device info, Python can access LJM. If import or open fails, re-check the LJM runtime installation.

Safety first — use dry-run
--------------------------
Before writing to hardware, always perform dry-run tests. The skeleton supports a --dry-run flag that prevents any LJM calls and instead prints intended writes and writes logs. This is the recommended safe workflow.

Quick dry-run examples (from repo root)
- Set all channels to 2.5 V (dry-run):
  python -m src.set_tdac ALL 2.5 --dry-run

- Set a single channel constant (dry-run):
  python -m src.set_tdac TDAC5=1.234 --dry-run

- Set a ramp on TDAC0 (dry-run):
  python -m src.set_tdac TDAC0=RAMP,0,5,0.1,100 --dry-run

- Use a profile file (INI or CSV) (dry-run):
  python -m src.set_tdac Profile.ini --dry-run

Expected dry-run behavior
- Console output showing intended register writes in the form:
  [DRY-RUN] 1615567123.123 WRITE DAC0 (TDAC0) = 2.5
- Logs under logs/ with a CSV of per-update values and a TXT event log.

Register mapping (important)
----------------------------
The TDACManager uses a register_map to translate logical TDAC indices (0..21) to LJM register names.
- By default, the skeleton uses a simple mapping DAC0 .. DAC21. This is a placeholder and MUST be verified and updated for your hardware. The correct register names depend on the T7/LJTick-DAC configuration and the manufacturer's register naming.

To supply the correct mapping:
1. Edit src/set_tdac.py or create a small helper to load a JSON register map and pass it to TDACManager, for example:

   from tdac_manager import TDACManager
   import json
   mapping = json.load(open('register_map.json'))
   tdac = TDACManager(dry_run=False, register_map={int(k):v for k,v in mapping.items()})

2. Or modify the default mapping in src/tdac_manager.py by replacing the default register_map initialization.

Example register_map.json structure
{
  "0": "LJT7_DAC0",
  "1": "LJT7_DAC1",
  "2": "LJT7_DAC2",
  ...
  "21": "LJT7_DAC21"
}

How to discover the correct register names
- Consult LabJack T7 and LJTick-DAC documentation for register names used by your firmware.
- Use an interactive Python session (careful: perform reads only; do not write until you confirm names):

python - <<'PY'
import labjack.ljm as ljm
h = ljm.openS('T7','USB','')
print('Handle info:', ljm.getHandleInfo(h))
# Attempt to read a safe register (device info) to confirm communication
print('Serial Number:', ljm.eReadName(h,'SERIAL_NUMBER'))
ljm.close(h)
PY

If you are unsure which names correspond to LJTick-DAC outputs, consult the LJTick-DAC documentation or LabJack support.

First hardware test (recommended minimal steps)
1. Install LJM runtime and labjack-ljm Python package (see above).
2. Connect T7-Pro to the PC via USB and power the LJTick-DAC modules as required.
3. Keep a voltmeter connected to one DAC output to verify physical voltage change.
4. Start with a single-channel write with a safe small voltage. Use the TDACManager with dry_run=False and a verified register_map.

Example minimal test script (edit register_map first):

python - <<'PY'
from tdac_manager import TDACManager
# Example mapping for TDAC0 only; replace 'DAC0' with actual register name
m = {0: 'DAC0'}
manager = TDACManager(dry_run=False, register_map=m)
manager.open()
try:
    manager.write_values({0: 1.0})
    print('Wrote 1.0 V to TDAC0')
    val = manager.read_value(0)
    print('Read back:', val)
finally:
    manager.close()
PY

If this successfully writes and the voltmeter shows the expected voltage, proceed gradually to more channels.

CLI usage summary
-----------------
- python -m src.set_tdac [COMMANDS] [--dry-run] [--update-ms N] [--verbose]

Command token patterns supported by the skeleton:
- ALL <spec> — apply <spec> to all channels (e.g., ALL 2.5)
- TDACn <spec> — set TDACn to a specification (e.g., TDAC5 2.5 or TDAC5=2.5)
- TDACn=CONST,1.2 or TDACn=1.2 — constant
- TDACn=RAMP,start,end,step,delay_ms
- TDACn=SINE,offset,amplitude,frequency,phase
- TDACn=PULSE,low,high,period_ms,duty
- TDACn=RANDOM,min,max,update_ms,seed
- Profile file: pass a .ini or .csv filename as the first argument

Examples
- Set two channels to constants (dry-run):
  python -m src.set_tdac TDAC0=1.2 TDAC1=2.3 --dry-run

- Set a range (TDAC0..TDAC10) to 3.3 V (future support):
  python -m src.set_tdac TDAC0 TDAC10 3.3 --dry-run

Logging
-------
- Runtime data logged in logs/ by default. CSV contains timestamp, tdac_id, voltage, status. TXT contains events and errors.
- Adjust logging location by editing src/config.py (DEFAULT_CONFIG['logging']['path']).

Emergency stop and shutdown
---------------------------
- Press Ctrl+C during execution. The skeleton handles SIGINT and will stop the scheduler and close the device handle.
- Configure shutdown behavior (hold, zero, restore) in future enhancements — currently the skeleton closes the device and leaves outputs as-is (or follow your hardware safe defaults).

Troubleshooting
---------------
- "labjack.ljm import error": Ensure LJM runtime installed and labjack-ljm pip package installed. Reboot after runtime installation if needed.
- "Failed to open device": Confirm device is connected, powered, and drivers installed. Use LabJack utilities to verify device visibility.
- Unexpected voltages: Verify register mapping and measure with a DMM before commanding high voltages.
- Timing not accurate at 1ms update: Windows scheduling and Python may not guarantee 1ms real-time. Test and consider increasing update interval.

Extending the tool
------------------
- Add new waveform types by implementing a class inheriting from Waveform in src/waveforms.py and registering/creating it from the CLI/profile parser.
- Improve profile parsing in src/profile_loader.py to fully map profile entries to Channel and Waveform instances.
- Add a register_map.json loader and a config.ini implementation in src/config.py for runtime configuration without editing code.

Support and references
----------------------
- LabJack support & LJM documentation: https://labjack.com/support/software
- LJTick-DAC documentation (manufacturer) — consult for exact register names and wiring details.

If you would like, next steps I can take for you:
- Populate a best-effort default register_map using LabJack naming conventions and add an example register_map.json file to the repo.
- Implement profile-to-channel mapping so profiles can be executed end-to-end.
- Run a dry-run demo here in the workspace to produce logs and show sample output.


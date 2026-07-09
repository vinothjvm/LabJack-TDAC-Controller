LabJack T7-Pro TDAC Controller — Software Requirements Specification (SRS)

1. Introduction

1.1 Purpose
This document defines the software requirements for a Windows command-line application to control 22 independent analog outputs using a LabJack T7-Pro with 11 × LJTick-DAC modules over USB. The application will simulate analog signals for the Triconex 3703 EAI module during Verification & Validation (V&V) testing.

1.2 Scope
The application will:
- Run on Windows with Python 3.x and use the LabJack LJM driver.
- Control 22 TDAC outputs (TDAC0..TDAC21).
- Provide CLI and profile-driven operation (INI/CSV).
- Support multiple waveform types per channel and mixed operation.
- Offer logging, diagnostics, safety limits, and configurable timing.

1.3 Definitions, acronyms and abbreviations
- TDAC: Target DAC logical channel (TDAC0..TDAC21)
- LJM: LabJack Multiplexer / LabJack LJM library
- V&V: Verification & Validation

2. Overall description

2.1 Hardware
Supported Hardware:
- LabJack T7-Pro (1)
- LJTick-DAC (11)
- USB connection to host Windows PC

2.2 User characteristics
Users are engineers performing automated V&V tests. Familiarity with command-line tools and LabJack hardware is assumed.

2.3 Constraints
- Application targets Windows (Python 3.x) and LJM library availability.
- Timing accuracy depends on OS scheduling and LJM latency; the app provides configurable update periods (1ms .. 100ms) but the minimum reliable update rate depends on host capabilities and LJM.

3. Functional requirements

3.1 Device management
- Auto-detect connected T7-Pro devices over USB.
- Allow optional serial-number selection.
- Display device info: serial number, firmware version, connection type.

3.2 Channel mapping
- 22 logical TDAC outputs mapped across 11 LJTick-DAC modules:
  - TDAC0 -> DAC A module 1
  - TDAC1 -> DAC B module 1
  - ...
  - TDAC21 -> DAC B module 11

3.3 Operating modes and CLI
- Mode examples supported by CLI:
  - SetTDAC.py ALL 2.5
  - SetTDAC.py TDAC5 2.5
  - SetTDAC.py TDAC0 TDAC10 3.3
  - SetTDAC.py TDAC0=1.2 TDAC1=2.3
  - SetTDAC.py TDAC0=RAMP,0,5,0.1,100
  - SetTDAC.py Profile.ini
- Profile files: INI and CSV

3.4 Waveforms (per channel)
Each channel supports: Constant, Ramp, Triangle, Saw, Sine, Pulse, Random. User-defined waveforms are planned for the future.

3.5 Waveform parameters
- Ramp: start, end, step, delay(ms), repeat, direction, bidirectional
- Sine: offset, amplitude, frequency, phase, repeat
- Pulse: low, high, period, duty_cycle, repeat
- Random: min, max, update_time, seed, repeat

3.6 Scheduling and timing
- User-selectable update period: 1ms, 5ms, 10ms, 20ms, 50ms, 100ms or custom.
- Each scheduler tick computes next output for active channels and writes them in batches.

3.7 Logging
- CSV and TXT logging formats including timestamp, voltage, status, errors.
- Verbose/debug logging option.

3.8 Safety and error handling
- Configurable voltage clamps (presets: 0..5V, -5..5V, 0..10V, -10..10V or custom).
- Emergency stop (Ctrl+C) with configurable shutdown action (hold, zero, restore safe values).
- Handle and report: invalid register, invalid voltage, communication errors, USB disconnect, timeout, LJM exceptions — with retry logic.
- Verify write by read-back and report mismatch errors.

3.9 Diagnostics
- Dry-run mode (parse and simulate without writing to hardware).
- Show performance statistics (actual update rate).

3.10 Extensibility
- Plugin-style waveform architecture enabling new waveform types without changing scheduler/hardware abstraction.

4. Non-functional requirements

4.1 Performance
- Scheduler supports update rates down to 1ms if host and LJM can sustain the workload; target typical operation at 5–20ms.

4.2 Reliability
- Retry transient LJM errors; configurable retry count and backoff.

4.3 Usability
- Clear CLI usage and profile formats; concise runtime logging for V&V traceability.

4.4 Maintainability
- Modular design (parser, profile loader, waveform generators, scheduler, hardware manager, logger) with clear interfaces.

4.5 Portability
- Primary target: Windows. Codebase written in Python 3.x to ease future porting to other OSes.

5. Traceability matrix
(High-level mapping between SRS sections and design modules)
- Device management -> tdac_manager.py
- CLI and parser -> set_tdac.py, profile_loader.py
- Waveforms -> waveforms.py
- Channels -> channel.py
- Scheduler -> set_tdac.py / scheduler module
- Logging -> logger.py
- Configuration -> config.py

6. Appendices
- CLI examples and profile file reference will be provided in the SDD and user guide.

Revision history
- 2026-07-09: Initial SRS derived from consolidated requirements provided by the stakeholder.

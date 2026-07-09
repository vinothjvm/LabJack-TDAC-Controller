LabJack T7-Pro TDAC Controller — Software Design Document (SDD)

1. Overview
This document describes the software architecture and design decisions for the TDAC controller application. It maps the SRS to concrete modules, interfaces, and implementation guidance.

2. High-level architecture

User
  └─> CLI Parser (set_tdac.py)
       └─> Profile Loader (profile_loader.py)
            └─> Configuration Manager (config.py)
                 └─> Channel objects (channel.py)
                      └─> Waveform engines (waveforms.py)
                 └─> Scheduler / Timing Engine (set_tdac.py)
                      └─> TDAC Output Manager (tdac_manager.py)
                           └─> LabJack LJM

3. Module descriptions

3.1 set_tdac.py (CLI & scheduler)
- Responsibilities:
  - Command-line parsing to accept single/multiple TDAC commands or profile filename.
  - Validate commands and parameters.
  - Construct channel configurations and start/stop scheduler.
  - Provide dry-run, verbose and emergency-stop handling.
- Scheduler implementation:
  - Use a high-resolution loop (time.perf_counter) to maintain user-specified update interval.
  - On each tick, iterate active channels to compute next value, collect values, and call TDAC manager to write them.
  - Collect timing statistics and log actual update rate.

3.2 profile_loader.py
- Responsibilities:
  - Parse INI and CSV profile formats.
  - Convert profile entries into channel configuration objects.
  - Validate parameter ranges and types.

3.3 config.py (Configuration Manager)
- Provide defaults:
  - voltage_limits presets, default update_rate, logging settings, retry counts.
- Load global config.ini if present and override defaults.

3.4 channel.py
- Channel class encapsulates per-TDAC state:
  - id (TDACx), active flag, waveform instance, current value, safety limits, logging and status.
- Provides methods:
  - compute_next(timestamp) -> next_voltage
  - reset(), pause(), resume()

3.5 waveforms.py
- Abstract Waveform base class with a consistent interface:
  - initialize(params)
  - next_value(dt) or next_value(time)
  - is_finished() / reset()
- Implementations:
  - ConstantWaveform
  - RampWaveform
  - SineWaveform
  - PulseWaveform
  - RandomWaveform
- Design note: waveform instances are small, pure-Python classes to enable plugin-style extension.

3.6 tdac_manager.py (Hardware Abstraction)
- Responsibilities:
  - Detect LabJack devices (auto-detect, serial selection).
  - Provide batch write API: write_tdac_values(dict(tdac_id->voltage)).
  - Provide read-back API: read_tdac_value(tdac_id).
  - Implement dry-run mode: log actions instead of calling LJM.
  - Retry/timeout strategy on LJM exceptions.
- Implementation notes:
  - Try to import labjack.ljm. If not available, fall back to dry-run and warn.
  - Use batch writes where possible for performance. The LJM write names will be the labjack register names for the LJTick-DAC outputs.

3.7 logger.py
- Provide CSV/TXT logging with configurable fields: timestamp, TDAC id, voltage, status, errors.
- Support verbose/debug logs to console and file.

4. Data model and mapping
- Logical TDAC index -> hardware register mapping function will be centralized in tdac_manager or a small mapping table.
- Example mapping function: module = index // 2 + 1; channel = 'A' if index%2==0 else 'B'; register_name = f"LJTDAC{module}_DAC{channel}" (actual LJM register names to be used per LabJack guide)

5. Timing and scheduler considerations
- Using time.perf_counter() and a sleep strategy that accounts for drift.
- For high-rate updates (1ms), consider a busy-wait fallback or use threaded/OS real-time facilities — documented as host-dependent.

6. Error handling
- Centralized exception types in core/exceptions.py (existing file in repo).
- Transient errors: retry up to configurable count with small backoff.
- Fatal errors: stop scheduler, perform configured shutdown action, and log error.

7. Safety
- Voltage clamp validated per-channel before writing.
- Emergency stop (SIGINT handling) triggers configured safe-state action: HOLD, ZERO, RESTORE.
- On USB disconnect, optionally attempt reconnection and stop outputs if reconnection fails beyond threshold.

8. Logging & diagnostics
- Main runtime log: CSV file with timestamps and values per update.
- Event log: TXT containing device events, errors, and CLI commands.
- Dry-run mode writes the same logs but no hardware writes.

9. Profiles and configuration formats
- INI profile example:
  [global]
  update_rate = 10
  [TDAC0]
  waveform = CONSTANT
  value = 1.2
  [TDAC1]
  waveform = RAMP
  start = 0
  end = 5
  step = 0.1
  delay_ms = 100

- CSV profile format: columns: tdac_id,waveform,param1,param2,...

10. Extensibility
- Waveform classes register with a factory to allow new waveform add-ins.
- Hardware abstraction isolates LJM specifics to tdac_manager.py.

11. Tests and verification
- Unit tests to validate waveform outputs for given parameters.
- Integration test (dry-run) to exercise CLI parsing and scheduler.

12. Implementation plan (phases)
- Phase 1: CLI parser, waveform classes (Constant, Ramp, Sine), channel manager, dry-run scheduler.
- Phase 2: tdac_manager with LJM integration, logging, INI/CSV loader.
- Phase 3: full feature set (pulse, random), error handling, performance tuning.

Appendix A — Example runtime flow
1. User runs: set_tdac.py Profile.ini
2. CLI parses profile and builds 22 channel objects.
3. Scheduler starts at configured update rate.
4. Each tick: channels compute next values; TDAC manager writes them; logger records values.
5. On Ctrl+C: handle signal, perform shutdown action and flush logs.

Revision history
- 2026-07-09: Initial SDD derived from consolidated requirements and SRS.

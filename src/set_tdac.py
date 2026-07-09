"""CLI entrypoint for the TDAC controller (simplified skeleton)

Usage examples (supported patterns):
  python -m src.set_tdac ALL 2.5
  python -m src.set_tdac TDAC5 2.5
  python -m src.set_tdac TDAC0 TDAC10 3.3
  python -m src.set_tdac TDAC0=1.2 TDAC1=2.3
  python -m src.set_tdac TDAC0=RAMP,0,5,0.1,100
  python -m src.set_tdac Profile.ini
"""
from __future__ import annotations
import argparse
import time
import signal
import sys
from typing import Dict

from config import load_config
from profile_loader import load_profile
from tdac_manager import TDACManager
from channel import Channel
from waveforms import ConstantWaveform, RampWaveform, SineWaveform, PulseWaveform, RandomWaveform
from logger import Logger

RUNNING = True


def signal_handler(sig, frame):
    global RUNNING
    print("SIGINT received, stopping...")
    RUNNING = False


def parse_cli_args(args):
    parser = argparse.ArgumentParser(prog='set_tdac')
    parser.add_argument('commands', nargs='+', help='TDAC commands or profile file')
    parser.add_argument('--dry-run', action='store_true', help='Do not write to hardware')
    parser.add_argument('--update-ms', type=int, default=10, help='Scheduler update interval in ms')
    parser.add_argument('--verbose', action='store_true')
    return parser.parse_args(args)


def parse_command_token(token: str):
    """Parse a single token such as 'TDAC5', 'TDAC0=1.2', or 'TDAC0=RAMP,0,5,0.1,100'"""
    if '=' in token:
        left, right = token.split('=', 1)
        return left, right
    return token, None


def build_waveform_from_spec(spec: str):
    # spec examples: '1.2' or 'RAMP,0,5,0.1,100' or 'SINE,offset,amp,freq,phase'
    if spec is None:
        return None
    parts = spec.split(',')
    key = parts[0].upper()
    if key in ('CONSTANT', 'C') and len(parts) >= 2:
        wf = ConstantWaveform()
        wf.initialize(value=float(parts[1]))
        return wf
    if key == 'RAMP' or key == 'R':
        # RAMP,start,end,step,delay_ms
        _, start, end, step, delay = parts + [0]*(5-len(parts))
        wf = RampWaveform()
        wf.initialize(start=float(start), end=float(end), step=float(step), delay_ms=float(delay))
        return wf
    if key == 'SINE':
        # SINE,offset,amplitude,frequency,phase
        _, offset, amp, freq, phase = parts + [0]*(5-len(parts))
        wf = SineWaveform()
        wf.initialize(offset=float(offset), amplitude=float(amp), frequency=float(freq), phase=float(phase))
        return wf
    if key == 'PULSE':
        # PULSE,low,high,period_ms,duty
        _, low, high, period, duty = parts + [0]*(5-len(parts))
        wf = PulseWaveform()
        wf.initialize(low=float(low), high=float(high), period=float(period)/1000.0, duty_cycle=float(duty))
        return wf
    if key == 'RANDOM':
        # RANDOM,min,max,update_ms,seed
        _, minimum, maximum, update_ms, seed = parts + [0]*(5-len(parts))
        wf = RandomWaveform()
        wf.initialize(minimum=float(minimum), maximum=float(maximum), update_time_ms=int(update_ms), seed=int(seed) if seed else None)
        return wf
    # if spec is a simple numeric string
    try:
        v = float(spec)
        wf = ConstantWaveform()
        wf.initialize(value=v)
        return wf
    except Exception:
        return None


def main(argv=None):
    global RUNNING
    args = parse_cli_args(argv if argv is not None else sys.argv[1:])
    config = load_config()
    log = Logger(base_path=config.get('logging', {}).get('path', 'logs'))
    tdac = TDACManager(dry_run=args.dry_run)

    # Build channels (22 channels)
    channels: Dict[int, Channel] = {i: Channel(i, min_v=config['voltage_limits'].min_v, max_v=config['voltage_limits'].max_v) for i in range(22)}

    # Interpret commands
    first = args.commands[0]
    if first.lower().endswith('.ini') or first.lower().endswith('.csv'):
        profile = load_profile(first)
        # TODO: convert profile entries into waveform/channel config
        print('Profile loaded (skeleton).')
    else:
        # parse tokens
        for token in args.commands:
            left, right = parse_command_token(token)
            if left.upper() == 'ALL' and right is not None:
                # set all channels to constant
                wf = build_waveform_from_spec(right)
                for ch in channels.values():
                    ch.set_waveform(wf)
            elif left.upper().startswith('TDAC') and right is None:
                # single TDAC without '=' implies query or simple set? treat as query
                print(f'Query or no-op for {left}')
            else:
                # left may be 'TDAC5' or 'TDAC0'
                if left.upper().startswith('TDAC'):
                    try:
                        idx = int(left[4:])
                        wf = build_waveform_from_spec(right)
                        if wf is not None:
                            channels[idx].set_waveform(wf)
                    except Exception as e:
                        print('Failed to parse token', token, e)

    # Open hardware
    tdac.open()

    signal.signal(signal.SIGINT, signal_handler)

    update_ms = args.update_ms
    update_s = update_ms / 1000.0
    last = time.perf_counter()
    print('Starting scheduler (skeleton). Press Ctrl+C to stop.')
    while RUNNING:
        now = time.perf_counter()
        dt = now - last
        if dt >= update_s:
            # compute values
            values = {}
            for idx, ch in channels.items():
                v = ch.compute_next(now, dt)
                values[idx] = v
                log.log_value(idx, v)
            # write batch
            try:
                tdac.write_values(values)
            except Exception as e:
                print('Write error', e)
                log.log_event(f'Write error: {e}')
            last = now
        else:
            time.sleep(max(0.0, update_s - dt))

    # Shutdown
    print('Shutting down scheduler...')
    tdac.close()
    print('Done.')


if __name__ == '__main__':
    main()

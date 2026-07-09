"""Hardware abstraction for LabJack T7-Pro and LJTick-DAC via LJM

This module provides a configurable mapping from logical TDAC indices (0..21) to
LJM register names and implements write/read methods using the labjack.ljm API
when available. If the LJM library is not present or dry_run=True, actions are
logged to stdout instead of being sent to hardware.
"""
from typing import Dict, Optional
import time

DRY_RUN = False

try:
    import labjack.ljm as ljm  # type: ignore
    LJM_AVAILABLE = True
except Exception:
    LJM_AVAILABLE = False
    # Running without labjack library forces dry-run
    DRY_RUN = True


class TDACManager:
    def __init__(self, dry_run: bool = False, serial: Optional[str] = None,
                 register_map: Optional[Dict[int, str]] = None,
                 retry_count: int = 3, backoff_ms: int = 50):
        """Create TDACManager.

        - dry_run: when True, no hardware writes are performed.
        - serial: optional device serial to open.
        - register_map: optional dict mapping tdac_index -> LJM register name.
                        If not provided a default mapping of 'DAC0'..'DAC21' is used.
        - retry_count/backoff_ms: retry strategy for transient errors.
        """
        self.dry_run = dry_run or DRY_RUN
        self.serial = serial
        self.handle = None
        self.device_info = None
        self.retry_count = int(retry_count)
        self.backoff_ms = int(backoff_ms)

        if not self.dry_run and not LJM_AVAILABLE:
            raise RuntimeError("LJM library not available; enable dry-run or install labjack-ljm")

        # default mapping: DAC0..DAC21 (user must verify these names for their hardware)
        if register_map is None:
            self.register_map = {i: f"DAC{i}" for i in range(22)}
        else:
            self.register_map = dict(register_map)

    def set_register_map(self, mapping: Dict[int, str]):
        """Replace or set the register map."""
        self.register_map = dict(mapping)

    def detect(self):
        if self.dry_run:
            return {"detected": False, "notice": "dry-run"}
        try:
            # listAll() returns arrays; keep it simple here
            a, b, c = ljm.listAll()
            return {"detected": True, "num_devices": len(a)}
        except Exception as e:
            return {"detected": False, "error": str(e)}

    def open(self):
        if self.dry_run:
            self.handle = None
            return
        try:
            # Open a T7 over USB. If serial provided, use it; else open first device.
            if self.serial:
                self.handle = ljm.openS("T7", "USB", self.serial)
            else:
                # empty string opens first available
                self.handle = ljm.openS("T7", "USB", "")
            self.device_info = ljm.getHandleInfo(self.handle)
        except Exception as e:
            # propagate to caller to handle
            raise RuntimeError(f"Failed to open device: {e}")

    def close(self):
        if self.dry_run or self.handle is None:
            return
        try:
            ljm.close(self.handle)
        except Exception:
            pass

    def tdac_register_name(self, tdac_index: int) -> str:
        """Return the LJM register name for a given logical TDAC index.

        If the mapping does not contain the index, raise KeyError.
        """
        if tdac_index not in self.register_map:
            raise KeyError(f"No register mapping for TDAC index {tdac_index}")
        return self.register_map[tdac_index]

    def write_values(self, values: Dict[int, float]):
        """Write multiple TDAC values.

        values: dict mapping tdac_index -> voltage
        Returns True on success or raises an exception on failure.
        """
        if self.dry_run:
            ts = time.time()
            for idx, v in values.items():
                name = self.register_map.get(idx, f"TDAC{idx}")
                print(f"[DRY-RUN] {ts:.3f} WRITE {name} (TDAC{idx}) = {v}")
            return True

        if self.handle is None:
            raise RuntimeError("Device handle not open. Call open() before write_values().")

        last_exc = None
        for attempt in range(1, self.retry_count + 1):
            try:
                # Write each value using ljm.eWriteName for clarity and safety.
                for idx, v in values.items():
                    name = self.tdac_register_name(idx)
                    # ljm.eWriteName(handle, name, value)
                    ljm.eWriteName(self.handle, name, float(v))
                return True
            except Exception as e:
                last_exc = e
                # simple backoff
                time.sleep(self.backoff_ms / 1000.0)
        # If we get here, all retries failed
        raise RuntimeError(f"Failed to write TDAC values after {self.retry_count} attempts: {last_exc}")

    def read_value(self, tdac_index: int) -> float:
        """Read back a TDAC register value via LJM and return as float."""
        if self.dry_run:
            return 0.0
        if self.handle is None:
            raise RuntimeError("Device handle not open. Call open() before read_value().")
        name = self.tdac_register_name(tdac_index)
        try:
            val = ljm.eReadName(self.handle, name)
            return float(val)
        except Exception as e:
            raise RuntimeError(f"Failed to read {name}: {e}")

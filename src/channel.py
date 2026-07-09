"""Channel object encapsulating a TDAC logical output and its waveform"""
from typing import Optional
from waveforms import Waveform

class Channel:
    def __init__(self, tdac_id: int, waveform: Optional[Waveform] = None, enabled: bool = True,
                 min_v: float = 0.0, max_v: float = 5.0):
        self.tdac_id = tdac_id
        self.waveform = waveform
        self.enabled = enabled
        self.min_v = min_v
        self.max_v = max_v
        self.current_value = 0.0

    def compute_next(self, t: float, dt: float) -> float:
        if not self.enabled or self.waveform is None:
            return self.current_value
        v = self.waveform.next_value(t, dt)
        # clamp
        v = max(self.min_v, min(self.max_v, v))
        self.current_value = v
        return v

    def set_waveform(self, waveform: Waveform):
        self.waveform = waveform
        if hasattr(self.waveform, 'reset'):
            self.waveform.reset()

    def stop(self):
        self.enabled = False

    def start(self):
        self.enabled = True

    def reset(self):
        if self.waveform and hasattr(self.waveform, 'reset'):
            self.waveform.reset()
        self.current_value = 0.0

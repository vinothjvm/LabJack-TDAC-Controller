"""Waveform implementations for TDAC channels"""
from __future__ import annotations
import math
import random
from typing import Optional

class Waveform:
    def __init__(self):
        pass

    def initialize(self, **params):
        raise NotImplementedError

    def next_value(self, t: float, dt: float) -> float:
        """Return next value given timestamp t and delta t"""
        raise NotImplementedError

    def is_finished(self) -> bool:
        return False

    def reset(self):
        pass


class ConstantWaveform(Waveform):
    def initialize(self, value: float = 0.0, repeat: bool = True):
        self.value = float(value)
        self.repeat = bool(repeat)

    def next_value(self, t: float, dt: float) -> float:
        return self.value


class RampWaveform(Waveform):
    def initialize(self, start: float, end: float, step: float, delay_ms: float = 0,
                   repeat: bool = True, bidirectional: bool = False):
        self.start = float(start)
        self.end = float(end)
        self.step = float(step)
        self.delay_ms = float(delay_ms)
        self.repeat = bool(repeat)
        self.bidirectional = bool(bidirectional)
        self.current = self.start
        self.direction = 1 if self.end >= self.start else -1
        self._finished = False

    def next_value(self, t: float, dt: float) -> float:
        if self._finished:
            return self.current
        self.current += self.direction * abs(self.step)
        if (self.direction > 0 and self.current >= self.end) or (self.direction < 0 and self.current <= self.end):
            if self.bidirectional:
                self.direction *= -1
                # swap start/end behavior
            elif self.repeat:
                self.current = self.start
            else:
                self._finished = True
        return self.current

    def is_finished(self) -> bool:
        return self._finished

    def reset(self):
        self.current = self.start
        self.direction = 1 if self.end >= self.start else -1
        self._finished = False


class SineWaveform(Waveform):
    def initialize(self, offset: float = 0.0, amplitude: float = 1.0, frequency: float = 1.0, phase: float = 0.0,
                   repeat: bool = True):
        self.offset = float(offset)
        self.amplitude = float(amplitude)
        self.frequency = float(frequency)
        self.phase = float(phase)
        self.repeat = bool(repeat)

    def next_value(self, t: float, dt: float) -> float:
        # sine: offset + amplitude * sin(2*pi*f*t + phase)
        return self.offset + self.amplitude * math.sin(2.0 * math.pi * self.frequency * t + self.phase)


class PulseWaveform(Waveform):
    def initialize(self, low: float, high: float, period: float, duty_cycle: float = 50.0, repeat: bool = True):
        self.low = float(low)
        self.high = float(high)
        self.period = float(period)
        self.duty = float(duty_cycle) / 100.0
        self.repeat = bool(repeat)
        self._t0 = 0.0

    def next_value(self, t: float, dt: float) -> float:
        if self.period <= 0:
            return self.low
        phase = ((t - self._t0) % self.period) / self.period
        return self.high if phase < self.duty else self.low


class RandomWaveform(Waveform):
    def initialize(self, minimum: float = 0.0, maximum: float = 5.0, update_time_ms: int = 100, seed: Optional[int] = None,
                   repeat: bool = True):
        self.min = float(minimum)
        self.max = float(maximum)
        self.update_time = float(update_time_ms) / 1000.0
        self.repeat = bool(repeat)
        self._rand = random.Random(seed)
        self._next_change = 0.0
        self._value = self._rand.uniform(self.min, self.max)

    def next_value(self, t: float, dt: float) -> float:
        if t >= self._next_change:
            self._value = self._rand.uniform(self.min, self.max)
            self._next_change = t + self.update_time
        return self._value

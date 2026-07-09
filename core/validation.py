"""
===============================================================================
Project : LabJack TDAC Controller
Target  : Triconex 3703 EAI Simulator
File    : validation.py
Version : 1.0.0

Description
-----------
Validation helper functions used throughout the application.

These routines perform common validation of TDAC channel numbers, voltages,
waveforms, update rates, and file paths.

===============================================================================
"""

from __future__ import annotations

from pathlib import Path
from typing import Union

from core.constants import (
    MIN_TDAC,
    MAX_TDAC,
    MIN_VOLTAGE,
    MAX_VOLTAGE,
    MIN_UPDATE_RATE_MS,
    MAX_UPDATE_RATE_MS,
    SUPPORTED_WAVEFORMS,
)

from core.exceptions import (
    InvalidTDACError,
    InvalidVoltageError,
    InvalidWaveformError,
    UpdateRateError,
    ConfigurationFileNotFoundError,
)


Number = Union[int, float]


def validate_tdac(tdac: int) -> int:
    """
    Validate TDAC channel number.

    Parameters
    ----------
    tdac : int
        TDAC channel number.

    Returns
    -------
    int
        Valid TDAC channel.

    Raises
    ------
    InvalidTDACError
    """

    if not isinstance(tdac, int):
        raise InvalidTDACError("TDAC must be an integer.")

    if tdac < MIN_TDAC or tdac > MAX_TDAC:
        raise InvalidTDACError(
            f"TDAC must be between {MIN_TDAC} and {MAX_TDAC}."
        )

    return tdac


def validate_voltage(voltage: Number) -> float:
    """
    Validate output voltage.
    """

    try:
        voltage = float(voltage)
    except Exception:
        raise InvalidVoltageError("Voltage must be numeric.")

    if voltage < MIN_VOLTAGE or voltage > MAX_VOLTAGE:
        raise InvalidVoltageError(
            f"Voltage must be between "
            f"{MIN_VOLTAGE:.3f}V and {MAX_VOLTAGE:.3f}V."
        )

    return voltage


def validate_waveform(name: str) -> str:
    """
    Validate waveform name.
    """

    if not isinstance(name, str):
        raise InvalidWaveformError("Waveform name must be a string.")

    waveform = name.upper()

    if waveform not in SUPPORTED_WAVEFORMS:
        raise InvalidWaveformError(
            f"Unsupported waveform '{name}'."
        )

    return waveform


def validate_update_rate(rate_ms: Number) -> int:
    """
    Validate scheduler update rate.
    """

    try:
        rate_ms = int(rate_ms)
    except Exception:
        raise UpdateRateError("Update rate must be an integer.")

    if rate_ms < MIN_UPDATE_RATE_MS or rate_ms > MAX_UPDATE_RATE_MS:
        raise UpdateRateError(
            f"Update rate must be between "
            f"{MIN_UPDATE_RATE_MS} and "
            f"{MAX_UPDATE_RATE_MS} ms."
        )

    return rate_ms


def validate_profile_file(filename: Union[str, Path]) -> Path:
    """
    Validate INI profile exists.
    """

    path = Path(filename)

    if not path.exists():
        raise ConfigurationFileNotFoundError(
            f"Profile '{filename}' not found."
        )

    return path


def clamp_voltage(voltage: Number) -> float:
    """
    Clamp voltage to the supported output range.
    """

    voltage = float(voltage)

    if voltage < MIN_VOLTAGE:
        return MIN_VOLTAGE

    if voltage > MAX_VOLTAGE:
        return MAX_VOLTAGE

    return voltage


def validate_tdac_range(start: int, end: int) -> tuple[int, int]:
    """
    Validate TDAC range.
    """

    validate_tdac(start)
    validate_tdac(end)

    if start > end:
        raise InvalidTDACError(
            "Start TDAC cannot be greater than End TDAC."
        )

    return start, end


def validate_yes_no(value: str) -> bool:
    """
    Convert YES/NO configuration value into bool.
    """

    value = value.strip().upper()

    if value in ("YES", "TRUE", "1"):
        return True

    if value in ("NO", "FALSE", "0"):
        return False

    raise ValueError(
        "Expected YES or NO."
    )
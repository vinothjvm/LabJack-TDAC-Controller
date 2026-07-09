"""
===============================================================================
Project : LabJack TDAC Controller
Target  : Triconex 3703 EAI Simulator
File    : exceptions.py
Version : 1.0.0

Description
-----------
Custom exception classes used throughout the application.
===============================================================================
"""

from __future__ import annotations


class TDACError(Exception):
    """
    Base exception for all TDAC Controller errors.
    """

    def __init__(self, message: str = "TDAC Controller Error"):
        super().__init__(message)


# ---------------------------------------------------------------------------
# Configuration Errors
# ---------------------------------------------------------------------------

class ConfigurationError(TDACError):
    """Configuration file is invalid."""


class ConfigurationFileNotFoundError(ConfigurationError):
    """Configuration file could not be found."""


class ConfigurationValueError(ConfigurationError):
    """Configuration value is invalid."""


# ---------------------------------------------------------------------------
# Parser Errors
# ---------------------------------------------------------------------------

class ParserError(TDACError):
    """Command line parsing error."""


class InvalidCommandError(ParserError):
    """Unsupported command."""


class InvalidArgumentError(ParserError):
    """Invalid command line argument."""


# ---------------------------------------------------------------------------
# Validation Errors
# ---------------------------------------------------------------------------

class ValidationError(TDACError):
    """Validation failure."""


class InvalidTDACError(ValidationError):
    """Invalid TDAC number."""


class InvalidVoltageError(ValidationError):
    """Voltage outside allowed range."""


class InvalidWaveformError(ValidationError):
    """Unsupported waveform."""


class InvalidRangeError(ValidationError):
    """Invalid TDAC range."""


# ---------------------------------------------------------------------------
# Hardware Errors
# ---------------------------------------------------------------------------

class HardwareError(TDACError):
    """Generic hardware error."""


class DeviceNotFoundError(HardwareError):
    """No compatible LabJack device found."""


class DeviceConnectionError(HardwareError):
    """Unable to connect to the LabJack."""


class DeviceCommunicationError(HardwareError):
    """Communication with the device failed."""


class RegisterWriteError(HardwareError):
    """Failed to write a LabJack register."""


class RegisterReadError(HardwareError):
    """Failed to read a LabJack register."""


# ---------------------------------------------------------------------------
# Scheduler Errors
# ---------------------------------------------------------------------------

class SchedulerError(TDACError):
    """Scheduler failure."""


class UpdateRateError(SchedulerError):
    """Invalid scheduler update rate."""


# ---------------------------------------------------------------------------
# Waveform Errors
# ---------------------------------------------------------------------------

class WaveformError(TDACError):
    """Waveform processing error."""


class WaveformConfigurationError(WaveformError):
    """Waveform configuration is invalid."""


# ---------------------------------------------------------------------------
# Profile Errors
# ---------------------------------------------------------------------------

class ProfileError(TDACError):
    """Profile execution error."""


class ProfileSectionMissingError(ProfileError):
    """Required INI section is missing."""


class ProfileSyntaxError(ProfileError):
    """INI syntax error."""


# ---------------------------------------------------------------------------
# Logging Errors
# ---------------------------------------------------------------------------

class LoggingError(TDACError):
    """Logging system error."""


# ---------------------------------------------------------------------------
# Sequence Errors
# ---------------------------------------------------------------------------

class SequenceError(TDACError):
    """Sequence execution error."""


class SequenceStepError(SequenceError):
    """Invalid sequence step."""
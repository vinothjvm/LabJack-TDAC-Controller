"""
===============================================================================
Project : LabJack TDAC Controller
Target  : Triconex 3703 EAI Simulator
File    : constants.py
Version : 1.0.0
Author  : Vinoth Ravichandran

Description
-----------
Application wide constants.

===============================================================================
"""

from pathlib import Path

# ----------------------------------------------------------------------
# Project Information
# ----------------------------------------------------------------------

PROJECT_NAME = "LabJack TDAC Controller"

PROJECT_VERSION = "1.0.0"

PROJECT_DESCRIPTION = "LabJack T7-Pro TDAC Controller for Triconex 3703 EAI Simulator"

# ----------------------------------------------------------------------
# Supported Hardware
# ----------------------------------------------------------------------

DEVICE_TYPE = "T7"

DEFAULT_CONNECTION = "USB"

DEFAULT_IDENTIFIER = "ANY"

SUPPORTED_CONNECTIONS = [
    "USB",
    "ETHERNET",
    "WIFI"
]

# ----------------------------------------------------------------------
# TDAC Configuration
# ----------------------------------------------------------------------

MIN_TDAC = 0

MAX_TDAC = 21

TOTAL_TDAC = 22

MIN_VOLTAGE = 0.0

MAX_VOLTAGE = 5.0

DEFAULT_VOLTAGE = 0.0

# ----------------------------------------------------------------------
# Scheduler
# ----------------------------------------------------------------------

DEFAULT_UPDATE_RATE_MS = 20

MIN_UPDATE_RATE_MS = 1

MAX_UPDATE_RATE_MS = 1000

# ----------------------------------------------------------------------
# Logging
# ----------------------------------------------------------------------

LOG_DIRECTORY = "logs"

LOG_FILE_PREFIX = "TDAC"

LOG_FILE_EXTENSION = ".csv"

# ----------------------------------------------------------------------
# Profile Directory
# ----------------------------------------------------------------------

PROFILE_DIRECTORY = "profiles"

# ----------------------------------------------------------------------
# Example Directory
# ----------------------------------------------------------------------

EXAMPLE_DIRECTORY = "examples"

# ----------------------------------------------------------------------
# Documentation Directory
# ----------------------------------------------------------------------

DOCUMENT_DIRECTORY = "docs"

# ----------------------------------------------------------------------
# Root Folder
# ----------------------------------------------------------------------

ROOT_PATH = Path(__file__).resolve().parent.parent

LOG_PATH = ROOT_PATH / LOG_DIRECTORY

PROFILE_PATH = ROOT_PATH / PROFILE_DIRECTORY

DOCUMENT_PATH = ROOT_PATH / DOCUMENT_DIRECTORY

EXAMPLE_PATH = ROOT_PATH / EXAMPLE_DIRECTORY

# ----------------------------------------------------------------------
# Supported Waveforms
# ----------------------------------------------------------------------

WAVEFORM_CONSTANT = "CONSTANT"

WAVEFORM_RAMP = "RAMP"

WAVEFORM_TRIANGLE = "TRIANGLE"

WAVEFORM_SAW = "SAW"

WAVEFORM_SINE = "SINE"

WAVEFORM_PULSE = "PULSE"

WAVEFORM_RANDOM = "RANDOM"

SUPPORTED_WAVEFORMS = [
    WAVEFORM_CONSTANT,
    WAVEFORM_RAMP,
    WAVEFORM_TRIANGLE,
    WAVEFORM_SAW,
    WAVEFORM_SINE,
    WAVEFORM_PULSE,
    WAVEFORM_RANDOM
]

# ----------------------------------------------------------------------
# Exit Actions
# ----------------------------------------------------------------------

EXIT_HOLD = "HOLD"

EXIT_ZERO = "ZERO"

EXIT_PROFILE = "PROFILE"

# ----------------------------------------------------------------------
# Status
# ----------------------------------------------------------------------

STATUS_OK = "OK"

STATUS_WARNING = "WARNING"

STATUS_ERROR = "ERROR"

# ----------------------------------------------------------------------
# INI Sections
# ----------------------------------------------------------------------

SECTION_GENERAL = "General"

SECTION_HARDWARE = "Hardware"

SECTION_SCHEDULER = "Scheduler"

SECTION_LOGGING = "Logging"

SECTION_LIMITS = "Limits"

SECTION_SEQUENCE = "TestSequence"

SECTION_SHUTDOWN = "Shutdown"

# ----------------------------------------------------------------------
# Misc
# ----------------------------------------------------------------------

CSV_SEPARATOR = ","

INI_EXTENSION = ".ini"

CSV_EXTENSION = ".csv"

JSON_EXTENSION = ".json"

ENCODING = "utf-8"
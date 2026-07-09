"""Configuration defaults and loader for TDAC controller"""
from dataclasses import dataclass
from typing import Tuple

@dataclass
class VoltageLimits:
    min_v: float = 0.0
    max_v: float = 5.0

# Default configuration
DEFAULT_CONFIG = {
    "update_rate_ms": 10,
    "voltage_limits": VoltageLimits(0.0, 5.0),
    "logging": {
        "csv": True,
        "txt": True,
        "path": "logs/",
    },
    "retry": {
        "count": 3,
        "backoff_ms": 50,
    },
}


def load_config(path: str = None):
    """Placeholder for loading a global config.ini. For now, return defaults."""
    # TODO: implement reading from config.ini
    return DEFAULT_CONFIG

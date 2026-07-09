"""Profile loader for INI and CSV formats"""
import configparser
import csv
from typing import Dict, Any


def load_ini(path: str) -> Dict[str, Any]:
    cfg = configparser.ConfigParser()
    cfg.read(path)
    result = {}
    # example: each section corresponds to a TDAC or global
    for section in cfg.sections():
        result[section] = dict(cfg[section])
    return result


def load_csv(path: str) -> Dict[str, Any]:
    result = {}
    with open(path, newline='') as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            tdac = row.get('tdac_id') or row.get('TDAC') or row.get('id')
            if tdac:
                result[tdac] = row
    return result


def load_profile(path: str) -> Dict[str, Any]:
    if path.lower().endswith('.ini'):
        return load_ini(path)
    elif path.lower().endswith('.csv'):
        return load_csv(path)
    else:
        raise ValueError('Unsupported profile format')

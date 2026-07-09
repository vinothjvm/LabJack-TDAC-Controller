"""Simple CSV/TXT logger for TDAC controller"""
import csv
import os
import time
from typing import Optional, Dict

class Logger:
    def __init__(self, base_path: str = "logs", csv_enabled: bool = True, txt_enabled: bool = True):
        self.base_path = base_path
        self.csv_enabled = csv_enabled
        self.txt_enabled = txt_enabled
        os.makedirs(self.base_path, exist_ok=True)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        self.csv_file = os.path.join(self.base_path, f"tdac_log_{timestamp}.csv")
        self.txt_file = os.path.join(self.base_path, f"tdac_events_{timestamp}.txt")
        if self.csv_enabled:
            with open(self.csv_file, 'w', newline='') as fh:
                writer = csv.writer(fh)
                writer.writerow(['timestamp','tdac_id','voltage','status'])

    def log_value(self, tdac_id: int, voltage: float, status: str = 'OK'):
        ts = time.time()
        if self.csv_enabled:
            with open(self.csv_file, 'a', newline='') as fh:
                writer = csv.writer(fh)
                writer.writerow([f"{ts:.6f}", tdac_id, voltage, status])
        if self.txt_enabled:
            with open(self.txt_file, 'a') as fh:
                fh.write(f"{ts:.6f} TDAC{tdac_id} = {voltage} ({status})\n")

    def log_event(self, message: str):
        ts = time.time()
        if self.txt_enabled:
            with open(self.txt_file, 'a') as fh:
                fh.write(f"{ts:.6f} EVENT: {message}\n")

from dataclasses import dataclass
from typing import List
from .scanner import ScanRow

"""Dataclass for holding the structured scan results."""

palette = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 
                     'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan']

@dataclass
class ScanResult:
    ssid: str
    channel: int
    bandwidth: int
    rssi: int  # dBm

    @property
    def color(self) -> str:
        # Im using a hash of the SSID to get the same colors for the same network
        return palette[hash(self.ssid) % len(palette)]


def to_results(rows: List[ScanRow]) -> List[ScanResult]:
    return [ScanResult(*r) for r in rows]
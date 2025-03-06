from dataclasses import dataclass
from typing import List
from .scanner import ScanRow

"""Dataclass for holding the structured scan results."""

@dataclass
class ScanResult:
    ssid: str
    channel: int
    rssi: int  # dBm

    @property
    def color(self) -> str:
        palette = [
            "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
            "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf",
        ]
        return palette[self.channel % len(palette)]


def to_results(rows: List[ScanRow]) -> List[ScanResult]:
    return [ScanResult(*r) for r in rows]
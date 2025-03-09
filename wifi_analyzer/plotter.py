from __future__ import annotations
import matplotlib.pyplot as plt
import numpy as np
from typing import List
from .parser import ScanResult

"""Real‑time matplotlib visualisation! Looks so cool"""

class LivePlot:
    def __init__(self):
        plt.style.use("dark_background")
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlabel("Channel")
        self.ax.set_ylabel("RSSI (dBm)")
        self.ax.set_xlim(-2, 16)
        self.ax.set_ylim(-100, -20)
        self.ax.set_xticks(range(1, 15))
        self.ax.set_yticks(range(-100, -19, 10))
        self.ax.grid(True, which="both", linestyle="--", alpha=0.3)

    def draw(self, results: List[ScanResult]):
        self.ax.cla()
        self.__init__()  # reset axes limits/grids
        for res in results:
            diff = 10 / 5  # 20 MHz (10/5 fudge factor)
            x = np.linspace(res.channel - diff, res.channel + diff, 50)
            y = (-100 - res.rssi) * np.sin((x - res.channel + 2) / diff * np.pi)
            y = -100 - y
            self.ax.fill(x, y, color=res.color, alpha=0.3)
            self.ax.plot(x, y, color=res.color)
            self.ax.text(res.channel, res.rssi + 1, res.ssid, ha="center", fontsize=8)
        plt.pause(0.01)
from __future__ import annotations
import matplotlib.pyplot as plt
import numpy as np
from typing import List
from .parser import ScanResult, palette

"""Real‑time matplotlib visualisation! Looks so cool"""

class LivePlot:
    def __init__(self):
        plt.style.use("dark_background")
        self.fig = plt.figure(figsize=(10, 6))
        self.ax = self.fig.add_subplot(111)
        self._setup_axes()
        
        self.fig.set_tight_layout(True)
        
    def _setup_axes(self):
        """Configure the plot axes with standard settings"""
        self.ax.set_xlabel("Wi-Fi Channel")
        self.ax.set_ylabel("RSSI [dBm]")
        self.ax.set_xlim(-2, 16)
        self.ax.set_ylim(-99, -20)
        
        x_major_ticks = np.arange(0, 16, 1)
        self.ax.set_xticks(x_major_ticks)
        
        y_major_ticks = np.arange(-20, -100, -10)
        self.ax.set_yticks(y_major_ticks)
        
        self.ax.grid(axis='y', linestyle='--')
        self.ax.grid(axis='x', linestyle=':', color='r', alpha=0.3)

    def draw(self, results: List[ScanResult]):
        self.ax.cla()
        self._setup_axes()
        
        if not results:
            self.ax.text(7, -60, "No WiFi networks found", 
                        ha="center", fontsize=14, color="white")
            plt.pause(0.01)
            return
        
            
        for index, res in enumerate(results):
            diff = res.bandwidth / 5  
            x = np.linspace(res.channel - diff, res.channel + diff, 50)
            y = (-99 - res.rssi) * np.sin((x - res.channel + 2) / diff * np.pi)
            y = -99 - y
            
            color = palette[index % len(palette)]
            
            self.ax.fill(x, y, color=color, alpha=0.3)
            self.ax.plot(x, y, color=color)
            self.ax.text(res.channel, res.rssi + 1, res.ssid, ha="center", fontsize=8)
    
        plt.draw()
        plt.pause(0.01)
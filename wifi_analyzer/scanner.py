from __future__ import annotations
import platform
import subprocess
import re
from typing import List, Tuple


ScanRow = Tuple[str, int, int, int]  # SSID, channel, bandwidth, RSSI

class WiFiScanner:
    """Runs a single scan and returns list of (ssid, channel, rssi)."""

    def scan(self) -> List[ScanRow]:
        system = platform.system()
        if system == "Darwin":
            return _scan_macos()
        if system == "Linux":
            return _scan_linux()
        raise NotImplementedError(f"Unsupported OS: {system}")


"""These are the platform‑specific Wi‑Fi scan executors. No windows support atm."""


def _scan_macos() -> List[ScanRow]:
    cmd = (
        'system_profiler SPAirPortDataType'
        ' | grep -A 9999 "Other Local Wi-Fi Networks:"')
    
    proc = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    stdoutlines = [line.lstrip() for line in proc.stdout.split('\n')]
    
    scanned_ssid = []
    for line in stdoutlines:
        if line.endswith(':') and stdoutlines.index(line) != 0:
            scanned_ssid.append(line.split(':')[0])
        if line.startswith('Channel:'):
            channel = re.search(r'Channel: \d+', line)
            if channel:
                res = channel.group().split()
                scanned_ssid.append(res[-1])
            bandwidth = re.search(r'\d+MHz', line)
            if bandwidth:
                res = bandwidth.group().split('MHz')
                scanned_ssid.append(res[0])
        if line.startswith('Signal / Noise:'):
            rssi = re.search(r'-\d+', line)
            if rssi:
                res = rssi.group().split()
                scanned_ssid.append(res[0])

    rows = []
    for i in range(0, len(scanned_ssid), 4):
        if i + 3 < len(scanned_ssid):
            try:
                ssid = scanned_ssid[i]
                channel = int(scanned_ssid[i+1])
                bandwidth = int(scanned_ssid[i+2])
                rssi = int(scanned_ssid[i+3])
                rows.append((ssid, channel, bandwidth, rssi))
            except (ValueError, IndexError) as e:
                print(f"Error processing entry at index {i}: {e}")
                continue
    
    print(f"Found {len(rows)} networks")
    return rows


def _scan_linux() -> List[ScanRow]:
    cmd = 'sudo iwlist scanning'
    proc = subprocess.run(cmd.split(), capture_output=True, text=True)
    lines = proc.stdout.splitlines()

    rows: List[ScanRow] = []
    ssid, channel, rssi, bandwidth = None, None, None, 20
    for line in lines:
        line = line.strip()
        if 'ESSID:"' in line:
            ssid = line.split('ESSID:"')[1].rstrip('"')
        elif "Channel " in line:
            channel = int(line.split("Channel ")[1])
        elif "Signal level=" in line:
            rssi = int(line.split("Signal level=")[1].split(' dBm')[0])
            if ssid and channel and rssi:
                rows.append((ssid, channel, bandwidth, rssi))
                ssid, channel, rssi, bandwidth = None, None, None, 20
    return rows
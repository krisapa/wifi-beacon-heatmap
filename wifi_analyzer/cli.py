import argparse
import csv
import time
from pathlib import Path
from typing import Optional

from .scanner import WiFiScanner
from .parser import to_results
from .plotter import LivePlot
from .utils import default_log_path

"""CLI run."""

def run(interval: float, duration: Optional[int], log: bool):
    scanner = WiFiScanner()
    plot = LivePlot()

    log_path: Optional[Path] = default_log_path() if log else None
    writer = None
    if log_path:
        log_path.parent.mkdir(exist_ok=True, parents=True)
        csv_file = log_path.open("w", newline="")
        writer = csv.writer(csv_file)
        writer.writerow(["timestamp", "ssid", "channel", "rssi"])
        print(f"Logging to {log_path}")

    start = time.time()
    try:
        while True:
            rows = scanner.scan()
            results = to_results(rows)
            plot.draw(results)
            now = time.time()
            if writer:
                for r in results:
                    writer.writerow([int(now), r.ssid, r.channel, r.rssi])
            if duration and (now - start) >= duration:
                break
            time.sleep(interval)
    finally:
        if writer:
            csv_file.close()


def main():
    ap = argparse.ArgumentParser(description="Wi‑Fi Spectrum Analyzer")
    ap.add_argument("--interval", type=float, default=2, help="scan interval seconds")
    ap.add_argument("--duration", type=int, help="exit after N seconds (default: run forever)")
    ap.add_argument("--log", action="store_true", help="save CSV log to ~/wifi_scans")
    args = ap.parse_args()
    run(args.interval, args.duration, args.log)

if __name__ == "__main__":
    main()
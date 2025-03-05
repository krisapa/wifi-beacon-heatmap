from pathlib import Path
from datetime import datetime

def timestamp_now() -> str:
    """Returns current timestamp in YYYYmmdd_HHMMSS."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def default_log_path() -> Path:
    """Helper to get ~/wifi_scans/<timestamp>.csv path."""
    base = Path.home() / "wifi_scans"
    base.mkdir(exist_ok=True)
    return base / f"scan_{timestamp_now()}.csv"
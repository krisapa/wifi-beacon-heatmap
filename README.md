# WiFi Beacon Heatmap Analyzer

WiFi Beacon Heatmap Analyzer scans for nearby WiFi networks and visualizes their signal strength, channel, and bandwidth in real time. It works on macOS (using `system_profiler`) and Linux (using `iwlist`). The tool provides a live updating plot of the local wireless environment, and can optionally log scan results to CSV. The code is organized into separate files for scanning, parsing, and plotting.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/Platform-macOS%20%7C%20Linux-lightgrey.svg" alt="Platform Support">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
</p>

## Quick Start

### Prerequisites

- Python 3.9 or higher
- macOS or Linux (Windows support coming soon)
- On Linux: `wireless-tools` package for `iwlist` command

### Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/wifi-beacon-heatmap.git
cd wifi-beacon-heatmap
```

2. Create and activate a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Analyzer

Start the real-time WiFi analyzer:
```bash
python3 -m wifi_analyzer.cli --interval 2
```

The visualization window will open and refresh every 2 seconds. Press `Ctrl+C` to exit.

## Usage Options

```bash
# Basic usage - scan every 2 seconds
python3 -m wifi_analyzer.cli --interval 2

# Log scan results to CSV file
python3 -m wifi_analyzer.cli --interval 3 --log

# Run for a specific duration (30 seconds)
python3 -m wifi_analyzer.cli --interval 2 --duration 30

# Show help
python3 -m wifi_analyzer.cli --help
```


## Understanding the Visualization

The heatmap displays:
- **X-axis**: WiFi channels (1-14 for 2.4GHz, higher numbers for 5GHz)
- **Y-axis**: Signal strength in dBm (higher = stronger signal)
- **Colored curves**: Each network represented by a sine wave
- **Width**: Represents channel bandwidth (20MHz, 40MHz, 80MHz)
- **Labels**: Network names (SSIDs) displayed above each signal

## How It Works

1. Uses platform-specific tools to scan nearby WiFi networks
   - macOS: `system_profiler SPAirPortDataType`
   - Linux: `iwlist scanning`

2. Extract network information (SSID, channel, bandwidth, RSSI)

3. Plots signals as sine waves with:
   - Channel position on X-axis
   - Signal strength on Y-axis  
   - Bandwidth determining curve width

## Installation on Different Platforms

### macOS
No additional setup required - uses built-in `system_profiler`:


### Linux (Ubuntu/Debian)
Install wireless tools:
```bash
sudo apt-get install wireless-tools
python3 -m wifi_analyzer.cli --interval 2
```

### Linux (RHEL/CentOS/Fedora)
```bash
sudo yum install wireless-tools    # RHEL/CentOS
# or
sudo dnf install wireless-tools    # Fedora
python3 -m wifi_analyzer.cli --interval 2
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

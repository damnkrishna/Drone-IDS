#  Setup (ArduPilot + SITL + MAVProxy + QGroundControl)

This guide shows how to set up ArduPilot SITL, capture MAVLink telemetry with MAVProxy, visualize with QGroundControl, and convert telemetry logs (`.tlog`) to clean CSVs ready for analysis / ML training.

> Tone: encouraging, practical — do the steps exactly as shown. 

---

## Contents

1. Prerequisites & `requirements.txt`
2. Clone ArduPilot & create venv
3. Run SITL (ArduCopter)
4. Run MAVProxy (with logging)
5. Run QGroundControl (GUI) — launcher command updated
6. Capture & convert logs to CSV
7. Cleaning and splitting CSVs by message type
8. Labeling attacks (recommended)
9. Quick troubleshooting & tips

---

## 1) Prerequisites

Run updates and install system dependencies (Ubuntu/Debian):

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y git wget curl build-essential python3 python3-dev python3-venv python3-pip \
    libxml2-dev libxslt-dev libz-dev \
    libgstreamer1.0-dev gstreamer1.0-plugins-base gstreamer1.0-plugins-good \
    libqt5multimedia5-plugins qml-module-qtmultimedia \
    python3-wxgtk4.0  # optional, only if you want MAVProxy map module
```

> Some GUI libraries (wx) are optional — QGroundControl provides map/GUI, so you can skip wx if you don’t need MAVProxy map.

---

## 2) `requirements.txt`

Create a file `requirements.txt` in your project with this content:

```
future
pymavlink
MAVProxy
lxml
numpy
pandas
scikit-learn
```

Install into a Python venv (next section) with:

```bash
python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

---

## 3) Clone ArduPilot & set up virtualenv

```bash
git clone https://github.com/ArduPilot/ardupilot.git ~/ardupilot
cd ~/ardupilot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

(If you get errors during `pip install`, paste them here — I’ll give fixes.)

---

## 4) Run SITL (ArduCopter)

Open Terminal 1 (Simulator terminal). Activate venv and start SITL:

```bash
cd ~/ardupilot
source venv/bin/activate

# Start SITL (quadrotor)
Tools/autotest/sim_vehicle.py -v ArduCopter -f quad --console --map
```

This opens the SITL console and a map window (SITL's map). SITL listens on UDP port `14550` by default.

Keep this terminal open.

---

## 5) Run MAVProxy (command / logging)

Open Terminal 2 (Command terminal). Activate venv and start MAVProxy with explicit logging and forwarding:

```bash
cd ~/ardupilot
source venv/bin/activate

# Start MAVProxy, forward to 14551 for QGC, and write a tlog
mkdir -p ~/drone_logs
mavproxy.py --master=udp:127.0.0.1:14550 --out=udp:127.0.0.1:14551 --logfile ~/drone_logs/mavproxy_$(date +%F_%H%M%S).tlog
```

* `--master` connects MAVProxy to SITL.
* `--out` forwards MAVLink to QGroundControl on port `14551`.
* `--logfile` creates a `.tlog` file in `~/drone_logs`.

Use this terminal to type commands:

```
mode GUIDED
arm throttle
takeoff 10
rtl
land
status
```

---

## 6) Run QGroundControl (GUI)

Open Terminal 3 (GUI launcher) and run:

```bash
# make sure QGroundControl AppImage is executable
chmod +x ~/QGroundControl-x86_64.AppImage 2>/dev/null || true

# start QGroundControl
./QGroundControl-x86_64.AppImage
```

> Important: use `./QGroundControl-x86_64.AppImage` as the launcher. QGC should auto-detect SITL or connect to `udp:127.0.0.1:14551` (if using MAVProxy). If not, click the top banner, choose UDP and enter port `14551` (or `14550` if connecting directly to SITL).

---

## 7) Capture logs (what files you get)

* MAVProxy tlog: `~/drone_logs/mavproxy_YYYY-MM-DD_HHMMSS.tlog` (binary MAVLink trace).
* SITL may also generate DataFlash logs (`.bin`) under `~/ardupilot/logs` or similar.
* QGroundControl logs (download via GUI Analyze → Logs).

These `.tlog` files are the canonical logs containing every MAVLink message you sent/received, including STATUSTEXT markers, HEARTBEAT, COMMAND\_LONG, GPS, ATTITUDE, etc.

---

## 8) Decode tlog → CSV (useful commands)

### Option A — Use built-in `mavlogdump.py` (preferred if present)

```bash
# Example: extract common types into a CSV
python3 ~/ardupilot/modules/mavlink/pymavlink/tools/mavlogdump.py \
  --types ATTITUDE,GPS_RAW_INT,GLOBAL_POSITION_INT,SYS_STATUS,RC_CHANNELS \
  --format csv ~/drone_logs/mavproxy_YYYY-MM-DD_HHMMSS.tlog > mav_all.csv
```

Or dump everything (can be large):

```bash
python3 ~/ardupilot/modules/mavlink/pymavlink/tools/mavlogdump.py --format csv ~/drone_logs/mavproxy_*.tlog > mav_full.csv
```

---
- everything is stored in mav_all.csv -raw data

## 9) Clean & split CSV by message type (script)

Save this as `clean_mavlog_split.py` in the same folder and run it after `mav_all.csv` exists:

```python
#!/usr/bin/env python3
import pandas as pd

df = pd.read_csv("mav_all.csv")

message_types = ["ATTITUDE", "GPS_RAW_INT", "GLOBAL_POSITION_INT", "SYS_STATUS", "RC_CHANNELS"]

for msg in message_types:
    cols = [c for c in df.columns if c.startswith(msg)]
    if not cols:
        print(f"[!] No columns found for {msg}")
        continue
    cols = ["timestamp"] + cols if "timestamp" in df.columns else cols
    sub_df = df[cols].dropna(how="all")
    filename = f"{msg.lower()}_clean.csv"
    sub_df.to_csv(filename, index=False)
    print(f"[+] Saved {filename} with {len(sub_df)} rows and {len(sub_df.columns)} cols")
```

Run:

```bash
python3 clean_mavlog_split.py
```

This creates:

* `attitude_clean.csv`
* `gps_raw_int_clean.csv`
* `global_position_int_clean.csv`
* `sys_status_clean.csv`
* `rc_channels_clean.csv`

Each is tidy and contains only relevant fields for that message type — ready for visualization or ML feature extraction.

---

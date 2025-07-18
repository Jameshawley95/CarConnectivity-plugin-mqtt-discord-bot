import re
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from datetime import datetime
from datetime import timedelta

def format_timestamp(iso_str):
    try:
        dt = datetime.fromisoformat(iso_str)
        local_dt = dt.astimezone(ZoneInfo("Europe/London"))
        return local_dt.strftime("%H:%M:%S on %d %b %Y")
    except Exception:
        return "Unknown"

def extract_data(raw_log):
    fields = {
        "Battery Level": None,
        "Time to Full (min)": None,
        "Charging State": None,
        "Plug State": None,
        "Plug Lock": None,
        "Data Timestamp": None
    }

    # Catch the last timestamp seen
    timestamp_pattern = re.compile(r"'carCapturedTimestamp': '([^']+)'")
    soc_pattern = re.compile(r"'currentSOC_pct': (\d+)")
    time_remaining_pattern = re.compile(r"'remainingChargingTimeToComplete_min': (\d+)")
    charging_pattern = re.compile(r"'chargingState': '([^']+)'")
    plug_state_pattern = re.compile(r"'plugConnectionState': '([^']+)'")
    plug_lock_pattern = re.compile(r"'plugLockState': '([^']+)'")

    fields["Battery Level"] = soc_pattern.findall(raw_log)[-1] if soc_pattern.findall(raw_log) else None
    fields["Charging State"] = charging_pattern.findall(raw_log)[-1] if charging_pattern.findall(raw_log) else None
    fields["Time to Full (min)"] = time_remaining_pattern.findall(raw_log)[-1] if time_remaining_pattern.findall(raw_log) else None
    fields["Plug State"] = plug_state_pattern.findall(raw_log)[-1] if plug_state_pattern.findall(raw_log) else None
    fields["Plug Lock"] = plug_lock_pattern.findall(raw_log)[-1] if plug_lock_pattern.findall(raw_log) else None

    # Get the latest carCapturedTimestamp (most recent one)
    timestamps = timestamp_pattern.findall(raw_log)
    if timestamps:
        latest_ts = max(timestamps)
        parsed_ts = datetime.strptime(latest_ts, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        adjusted_ts = parsed_ts + timedelta(hours=1)
        fields["Data Timestamp"] = adjusted_ts.strftime("%H:%M:%S on %d %b %Y")

    return fields

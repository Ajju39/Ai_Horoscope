import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")


def get_timezone_data(lat: float, lon: float, timestamp: int | None = None):
    if timestamp is None:
        timestamp = int(time.time())

    url = "https://maps.googleapis.com/maps/api/timezone/json"
    params = {
        "location": f"{lat},{lon}",
        "timestamp": timestamp,
        "key": GOOGLE_MAPS_API_KEY
    }

    response = requests.get(url, params=params, timeout=20)
    data = response.json()

    if data.get("status") != "OK":
        raise ValueError(f"Could not fetch timezone: {data}")

    raw_offset = data.get("rawOffset", 0)
    dst_offset = data.get("dstOffset", 0)
    total_offset_seconds = raw_offset + dst_offset

    sign = "+" if total_offset_seconds >= 0 else "-"
    total_offset_seconds = abs(total_offset_seconds)
    hours = total_offset_seconds // 3600
    minutes = (total_offset_seconds % 3600) // 60
    utc_offset = f"{sign}{hours:02d}:{minutes:02d}"

    return {
        "time_zone_id": data.get("timeZoneId"),
        "time_zone_name": data.get("timeZoneName"),
        "utc_offset": utc_offset
    }
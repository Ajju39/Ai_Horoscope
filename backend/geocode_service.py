import os
import requests
from dotenv import load_dotenv

load_dotenv()

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")


def get_lat_lng(place: str):
    print("Loaded API key:", GOOGLE_MAPS_API_KEY[:10] + "..." if GOOGLE_MAPS_API_KEY else "NONE")

    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": place,
        "key": GOOGLE_MAPS_API_KEY
    }

    response = requests.get(url, params=params, timeout=20)
    data = response.json()

    print("Google response:", data)

    if data.get("status") != "OK" or not data.get("results"):
        raise ValueError(f"Could not geocode place: {place}")

    result = data["results"][0]
    location = result["geometry"]["location"]

    return {
        "formatted_address": result["formatted_address"],
        "latitude": location["lat"],
        "longitude": location["lng"]
    }
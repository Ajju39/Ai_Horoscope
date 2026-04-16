from fastapi.responses import JSONResponse
from supabase_service import save_horoscope, get_history_by_name
from ai_service import generate_ai_horoscope
from timezone_service import get_timezone_data
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from geocode_service import get_lat_lng
from astrology_service import get_astrology_data
from horoscope_rules import generate_horoscope_reading

app = FastAPI(title="Horoscope AI App")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class BirthDetails(BaseModel):
    name: str
    birth_date: str
    birth_time: str
    birth_place: str


@app.get("/")
def home():
    return {"message": "Horoscope backend is running"}


@app.post("/generate-horoscope")
def generate_horoscope(data: BirthDetails):
    try:
        location = get_lat_lng(data.birth_place)
        tz = get_timezone_data(
        location["latitude"],
        location["longitude"]
        )
        astro = get_astrology_data(
            data.birth_date,
            data.birth_time,
            location["latitude"],
            location["longitude"],
            tz["utc_offset"]
        )

        reading = generate_horoscope_reading(
            astro["sun_sign"],
            astro["moon_sign"],
            astro["ascendant"]
        )
        ai_text = generate_ai_horoscope(
                data.name,
                astro["sun_sign"],
                astro["moon_sign"],
                astro["ascendant"]
        )
        record = {
                    "name": data.name,
                    "birth_date": data.birth_date,
                    "birth_time": data.birth_time,
                    "birth_place": data.birth_place,
                    "formatted_address": location["formatted_address"],
                    "latitude": location["latitude"],
                    "longitude": location["longitude"],
                    "time_zone_id": tz["time_zone_id"],
                    "time_zone_name": tz["time_zone_name"],
                    "utc_offset": tz["utc_offset"],
                    "sun_sign": astro["sun_sign"],
                    "moon_sign": astro["moon_sign"],
                    "ascendant": astro["ascendant"],
                    "finance": reading["finance"],
                    "career": reading["career"],
                    "health": reading["health"],
                    "relationship": reading["relationship"],
                    "ai_horoscope": ai_text
                }
        save_horoscope(record)
        return {
            "name": data.name,
            "birth_date_received": data.birth_date,
            "birth_time_received": data.birth_time,
            "formatted_address": location["formatted_address"],
            "latitude": location["latitude"],
            "longitude": location["longitude"],
            "time_zone_id": tz["time_zone_id"],
            "time_zone_name": tz["time_zone_name"],
            "utc_offset": tz["utc_offset"],
            "sun_sign": astro["sun_sign"],
            "moon_sign": astro["moon_sign"],
            "ascendant": astro["ascendant"],
            "finance": reading["finance"],
            "career": reading["career"],
            "health": reading["health"],
            "relationship": reading["relationship"],
            "ai_horoscope": ai_text
             }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/history/{name}")
def get_user_history(name: str):
    try:
        rows = get_history_by_name(name)
        return JSONResponse(content={"history": rows})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
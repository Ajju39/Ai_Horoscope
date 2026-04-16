import swisseph as swe
from datetime import datetime


SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]


def degree_to_sign(deg: float) -> str:
    deg = deg % 360
    return SIGNS[int(deg // 30)]


def get_astrology_data(date_str: str, time_str: str, lat: float, lon: float, utc_offset: str):
    year, month, day = map(int, date_str.split("-"))
    hour, minute = map(int, time_str.split(":"))

    # parse offset like +05:30 or -04:00
    sign = 1 if utc_offset[0] == "+" else -1
    off_h = int(utc_offset[1:3])
    off_m = int(utc_offset[4:6])
    offset_hours = sign * (off_h + off_m / 60.0)

    # local birth time -> UTC decimal hours
    local_decimal_hours = hour + minute / 60.0
    utc_decimal_hours = local_decimal_hours - offset_hours

    # adjust date if UTC crosses day boundary
    birth_dt = datetime(year, month, day)
    jd_ut = swe.julday(year, month, day, utc_decimal_hours)

    # Vedic / Sidereal Lahiri
    swe.set_sid_mode(swe.SIDM_LAHIRI, 0, 0)

    flags = swe.FLG_SIDEREAL

    sun_data = swe.calc_ut(jd_ut, swe.SUN, flags)[0]
    moon_data = swe.calc_ut(jd_ut, swe.MOON, flags)[0]

    houses = swe.houses_ex(jd_ut, lat, lon, b'P', flags)
    asc_degree = houses[1][0]

    sun_sign = degree_to_sign(sun_data[0])
    moon_sign = degree_to_sign(moon_data[0])
    asc_sign = degree_to_sign(asc_degree)

    return {
        "sun_sign": sun_sign,
        "moon_sign": moon_sign,
        "ascendant": asc_sign
    }
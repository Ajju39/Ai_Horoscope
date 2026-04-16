import swisseph as swe

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

    sign = 1 if utc_offset[0] == "+" else -1
    off_h = int(utc_offset[1:3])
    off_m = int(utc_offset[4:6])
    offset_hours = sign * (off_h + off_m / 60.0)

    local_decimal_hours = hour + minute / 60.0
    utc_decimal_hours = local_decimal_hours - offset_hours

    # handle UTC rollover
    while utc_decimal_hours < 0:
        utc_decimal_hours += 24
        jd_day_adjust = -1
        break
    else:
        jd_day_adjust = 0

    while utc_decimal_hours >= 24:
        utc_decimal_hours -= 24
        jd_day_adjust = 1
        break

    # compute julian day
    jd_ut = swe.julday(year, month, day + jd_day_adjust, utc_decimal_hours)

    # Lahiri sidereal mode
    swe.set_sid_mode(swe.SIDM_LAHIRI, 0, 0)
    flags = swe.FLG_SIDEREAL

    sun_deg = swe.calc_ut(jd_ut, swe.SUN, flags)[0][0]
    moon_deg = swe.calc_ut(jd_ut, swe.MOON, flags)[0][0]

    # houses_ex returns (cusps, ascmc)
    cusps, ascmc = swe.houses_ex(jd_ut, lat, lon, b'P', flags)
    asc_deg = ascmc[0]

    return {
        "sun_sign": degree_to_sign(sun_deg),
        "moon_sign": degree_to_sign(moon_deg),
        "ascendant": degree_to_sign(asc_deg)
    }
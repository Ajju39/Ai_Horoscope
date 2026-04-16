from flatlib.chart import Chart
from flatlib import const
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos



def get_astrology_data(date_str: str, time_str: str, lat: float, lon: float, utc_offset: str):
    year, month, day = date_str.split("-")
    flatlib_date = f"{day}/{month}/{year}"

    dt = Datetime(flatlib_date, time_str, utc_offset)
    pos = GeoPos(lat, lon)

    settings.set({
        "ayanamsha": const.AYANAMSHA_LAHIRI
    })

    chart = Chart(dt, pos, IDs=const.LIST_OBJECTS, hsys=const.HOUSES_PLACIDUS)

    sun = chart.get(const.SUN)
    moon = chart.get(const.MOON)
    asc = chart.get(const.ASC)

    return {
        "sun_sign": sun.sign,
        "moon_sign": moon.sign,
        "ascendant": asc.sign
    }
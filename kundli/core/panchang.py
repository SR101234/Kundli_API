"""Panchang calculation: Tithi, Vara, Nakshatra, Yoga, Karana, Sunrise, Sunset."""
from datetime import datetime, date, time
from typing import Dict, Any, List
import swisseph as swe
from pydantic import BaseModel
from kundli.core.nakshatra import get_nakshatra_from_longitude

TITHIS: List[str] = [
    "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami",
    "Shashthi", "Saptami", "Ashtami", "Navami", "Dashami",
    "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Purnima",
    "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami",
    "Shashthi", "Saptami", "Ashtami", "Navami", "Dashami",
    "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Amavasya"
]

VARAS: List[Dict[str, str]] = [
    {"day": "Monday", "lord": "Moon", "sanskrit": "Somavara"},
    {"day": "Tuesday", "lord": "Mars", "sanskrit": "Mangalavara"},
    {"day": "Wednesday", "lord": "Mercury", "sanskrit": "Budhavara"},
    {"day": "Thursday", "lord": "Jupiter", "sanskrit": "Guruvara"},
    {"day": "Friday", "lord": "Venus", "sanskrit": "Shukravara"},
    {"day": "Saturday", "lord": "Saturn", "sanskrit": "Shanivara"},
    {"day": "Sunday", "lord": "Sun", "sanskrit": "Ravivara"},
]

YOGAS: List[str] = [
    "Vishkambha", "Priti", "Ayushman", "Saubhagya", "Shobhana", "Atiganda",
    "Sukarma", "Dhriti", "Shoola", "Ganda", "Vriddhi", "Dhruva",
    "Vyaghata", "Harshana", "Vajra", "Siddhi", "Vyatipata", "Variyan",
    "Parigha", "Shiva", "Siddha", "Sadhya", "Shubha", "Shukla",
    "Brahma", "Indra", "Vaidhriti"
]

KARANA_FIXED = {
    57: "Shakuni",
    58: "Chatushpada",
    59: "Naga",
    60: "Kimstughna"
}
KARANA_REPEATING = ["Bava", "Balava", "Kaulava", "Taitila", "Gara", "Vanija", "Vishti"]


class PanchangResult(BaseModel):
    tithi_number: int
    tithi_name: str
    paksha: str
    tithi_percentage_left: float
    vara: str
    vara_lord: str
    nakshatra: str
    nakshatra_pada: int
    yoga: str
    yoga_number: int
    karana: str
    karana_number: int
    sunrise_time: str
    sunset_time: str


def calculate_panchang(
    tjd_ut: float,
    sun_lon: float,
    moon_lon: float,
    dt_local: datetime,
    latitude: float,
    longitude: float
) -> PanchangResult:
    """Calculate the 5 limbs of Panchang at the given moment."""
    # 1. Tithi (12 degrees per tithi)
    diff = (moon_lon - sun_lon) % 360.0
    tithi_idx = int(diff // 12.0)
    tithi_num = tithi_idx + 1
    tithi_name = TITHIS[tithi_idx]
    paksha = "Shukla Paksha" if tithi_num <= 15 else "Krishna Paksha"
    tithi_rem = 100.0 - ((diff % 12.0) / 12.0 * 100.0)

    # 2. Vara (Day)
    weekday_idx = dt_local.weekday()  # Monday is 0, Sunday is 6
    vara_info = VARAS[weekday_idx]

    # 3. Nakshatra of Moon
    moon_nak = get_nakshatra_from_longitude(moon_lon)

    # 4. Yoga ((Sun + Moon) % 360 / 13°20')
    yoga_span = 360.0 / 27.0
    sum_lon = (sun_lon + moon_lon) % 360.0
    yoga_idx = int(sum_lon // yoga_span)
    yoga_name = YOGAS[yoga_idx % 27]

    # 5. Karana (half of a tithi = 6 degrees)
    karana_idx = int(diff // 6.0) + 1  # 1 to 60
    if karana_idx == 1:
        karana_name = "Kimstughna"
    elif karana_idx in (58, 59, 60):
        karana_name = KARANA_FIXED.get(karana_idx, "Vishti")
    elif karana_idx == 57:
        karana_name = "Shakuni"
    else:
        # Repeating 7 karanas (indices 2 to 56)
        r_idx = (karana_idx - 2) % 7
        karana_name = KARANA_REPEATING[r_idx]

    # 6. Sunrise / Sunset
    try:
        rise_res = swe.rise_trans(
            tjd_ut - 0.5,
            swe.SUN,
            swe.CALC_RISE | swe.BIT_DISC_CENTER,
            (longitude, latitude, 0.0)
        )
        set_res = swe.rise_trans(
            tjd_ut - 0.5,
            swe.SUN,
            swe.CALC_SET | swe.BIT_DISC_CENTER,
            (longitude, latitude, 0.0)
        )
        # Convert JD to hour-minute string
        def jd_to_time_str(jd_val: float) -> str:
            rev_date = swe.revjul(jd_val)
            h = int(rev_date[3])
            m = int((rev_date[3] - h) * 60)
            return f"{h:02d}:{m:02d} UTC"
            
        sunrise_str = jd_to_time_str(rise_res[1][0])
        sunset_str = jd_to_time_str(set_res[1][0])
    except Exception:
        sunrise_str = "06:00 (approx)"
        sunset_str = "18:30 (approx)"

    return PanchangResult(
        tithi_number=tithi_num,
        tithi_name=tithi_name,
        paksha=paksha,
        tithi_percentage_left=round(tithi_rem, 2),
        vara=vara_info["sanskrit"],
        vara_lord=vara_info["lord"],
        nakshatra=moon_nak["nakshatra"],
        nakshatra_pada=moon_nak["nakshatra_pada"],
        yoga=yoga_name,
        yoga_number=yoga_idx + 1,
        karana=karana_name,
        karana_number=karana_idx,
        sunrise_time=sunrise_str,
        sunset_time=sunset_str
    )

"""Gochar (Transit) calculation of current planetary positions relative to natal chart."""
from datetime import datetime
from typing import Dict, Any, List
from kundli.astronomy.ephemeris import calculate_julian_day
from kundli.astronomy.planets import calculate_planet_positions
from kundli.core.zodiac import ZODIAC_SIGNS

# Benefic transit houses from natal Moon (Brihat Samhita)
BENEFIC_TRANSIT_HOUSES = {
    "Sun": [3, 6, 10, 11],
    "Moon": [1, 3, 6, 7, 10, 11],
    "Mars": [3, 6, 11],
    "Mercury": [2, 4, 6, 8, 10, 11],
    "Jupiter": [2, 5, 7, 9, 11],
    "Venus": [1, 2, 3, 4, 5, 8, 9, 11, 12],
    "Saturn": [3, 6, 11],
    "Rahu": [3, 6, 10, 11],
    "Ketu": [3, 6, 11]
}


def calculate_transits(
    natal_moon_sign_idx: int,
    natal_asc_sign_idx: int,
    transit_datetime: datetime = None,
    ayanamsa_name: str = "Lahiri"
) -> Dict[str, Any]:
    """Calculate current planetary transits and evaluate impact on natal Moon & Ascendant."""
    if transit_datetime is None:
        transit_datetime = datetime.now()

    tjd_ut = calculate_julian_day(transit_datetime)
    current_planets = calculate_planet_positions(tjd_ut, ayanamsa_name)

    transit_report = []
    for p_name, p in current_planets.items():
        # House from natal Moon
        h_from_moon = ((p.sign_index - natal_moon_sign_idx) % 12) + 1
        # House from natal Ascendant
        h_from_asc = ((p.sign_index - natal_asc_sign_idx) % 12) + 1

        benefic_houses = BENEFIC_TRANSIT_HOUSES.get(p_name, [3, 6, 11])
        is_favorable = h_from_moon in benefic_houses

        transit_report.append({
            "planet": p_name,
            "current_sign": p.sign,
            "current_degree": p.degree_in_sign,
            "retrograde": p.retrograde,
            "house_from_moon": h_from_moon,
            "house_from_ascendant": h_from_asc,
            "is_favorable": is_favorable,
            "status": "Favorable" if is_favorable else "Neutral / Adverse"
        })

    return {
        "transit_date": transit_datetime.strftime("%Y-%m-%d %H:%M:%S"),
        "ayanamsa": ayanamsa_name,
        "transits": transit_report
    }

"""Planetary calculation engine using Swiss Ephemeris."""
from typing import Dict, Any, List, Optional
import swisseph as swe
from pydantic import BaseModel
from kundli.astronomy.ayanamsa import configure_ayanamsa
from kundli.core.zodiac import get_sign_from_longitude
from kundli.core.nakshatra import get_nakshatra_from_longitude


class PlanetPosition(BaseModel):
    planet: str
    longitude: float
    latitude: float = 0.0
    distance: float = 0.0
    speed: float = 0.0
    retrograde: bool = False
    sign: str
    sign_index: int
    sign_lord: str
    degree_in_sign: float
    nakshatra: str
    nakshatra_index: int
    nakshatra_lord: str
    nakshatra_pada: int
    house: int = 1
    bhava_chalit_house: int = 1
    is_combust: bool = False


PLANET_MAP = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mars": swe.MARS,
    "Mercury": swe.MERCURY,
    "Jupiter": swe.JUPITER,
    "Venus": swe.VENUS,
    "Saturn": swe.SATURN,
    "Uranus": swe.URANUS,
    "Neptune": swe.NEPTUNE,
    "Pluto": swe.PLUTO,
}

COMBUSTION_ORBS = {
    "Moon": 12.0,
    "Mars": 17.0,
    "Mercury": 14.0,  # 12 when retrograde
    "Jupiter": 11.0,
    "Venus": 10.0,    # 8 when retrograde
    "Saturn": 15.0,
}


def calculate_planet_positions(
    tjd_ut: float,
    ayanamsa_name: str = "Lahiri",
    node_type: str = "mean",
    include_outer: bool = False
) -> Dict[str, PlanetPosition]:
    """Calculate sidereal positions for all planets."""
    sid_mode = configure_ayanamsa(ayanamsa_name)
    flag = swe.FLG_SWIEPH | swe.FLG_SPEED
    if sid_mode != -1:
        flag |= swe.FLG_SIDEREAL

    positions: Dict[str, PlanetPosition] = {}

    # Calculate 7 traditional planets
    for name, p_id in PLANET_MAP.items():
        if not include_outer and name in ("Uranus", "Neptune", "Pluto"):
            continue
        res, _ = swe.calc_ut(tjd_ut, p_id, flag)
        lon = res[0] % 360.0
        lat = res[1]
        dist = res[2]
        speed = res[3]
        retro = speed < 0.0 and name not in ("Sun", "Moon")

        sign_data = get_sign_from_longitude(lon)
        nak_data = get_nakshatra_from_longitude(lon)

        positions[name] = PlanetPosition(
            planet=name,
            longitude=round(lon, 4),
            latitude=round(lat, 4),
            distance=round(dist, 6),
            speed=round(speed, 6),
            retrograde=retro,
            sign=sign_data["sign"],
            sign_index=sign_data["sign_index"],
            sign_lord=sign_data["sign_lord"],
            degree_in_sign=round(sign_data["degree_in_sign"], 4),
            nakshatra=nak_data["nakshatra"],
            nakshatra_index=nak_data["nakshatra_index"],
            nakshatra_lord=nak_data["nakshatra_lord"],
            nakshatra_pada=nak_data["nakshatra_pada"]
        )

    # Calculate Rahu
    node_id = swe.MEAN_NODE if node_type == "mean" else swe.TRUE_NODE
    rahu_res, _ = swe.calc_ut(tjd_ut, node_id, flag)
    rahu_lon = rahu_res[0] % 360.0
    rahu_speed = rahu_res[3]
    rahu_retro = rahu_speed < 0.0 or node_type == "mean"

    rahu_sign = get_sign_from_longitude(rahu_lon)
    rahu_nak = get_nakshatra_from_longitude(rahu_lon)

    positions["Rahu"] = PlanetPosition(
        planet="Rahu",
        longitude=round(rahu_lon, 4),
        latitude=round(rahu_res[1], 4),
        distance=round(rahu_res[2], 6),
        speed=round(rahu_speed, 6),
        retrograde=rahu_retro,
        sign=rahu_sign["sign"],
        sign_index=rahu_sign["sign_index"],
        sign_lord=rahu_sign["sign_lord"],
        degree_in_sign=round(rahu_sign["degree_in_sign"], 4),
        nakshatra=rahu_nak["nakshatra"],
        nakshatra_index=rahu_nak["nakshatra_index"],
        nakshatra_lord=rahu_nak["nakshatra_lord"],
        nakshatra_pada=rahu_nak["nakshatra_pada"]
    )

    # Ketu is exactly 180 degrees opposite to Rahu
    ketu_lon = (rahu_lon + 180.0) % 360.0
    ketu_sign = get_sign_from_longitude(ketu_lon)
    ketu_nak = get_nakshatra_from_longitude(ketu_lon)

    positions["Ketu"] = PlanetPosition(
        planet="Ketu",
        longitude=round(ketu_lon, 4),
        latitude=round(-rahu_res[1], 4),
        distance=round(rahu_res[2], 6),
        speed=round(rahu_speed, 6),
        retrograde=rahu_retro,
        sign=ketu_sign["sign"],
        sign_index=ketu_sign["sign_index"],
        sign_lord=ketu_sign["sign_lord"],
        degree_in_sign=round(ketu_sign["degree_in_sign"], 4),
        nakshatra=ketu_nak["nakshatra"],
        nakshatra_index=ketu_nak["nakshatra_index"],
        nakshatra_lord=ketu_nak["nakshatra_lord"],
        nakshatra_pada=ketu_nak["nakshatra_pada"]
    )

    # Combustion check against Sun
    sun_lon = positions["Sun"].longitude
    for p_name, orb in COMBUSTION_ORBS.items():
        if p_name in positions:
            p_lon = positions[p_name].longitude
            diff = abs(p_lon - sun_lon)
            if diff > 180:
                diff = 360 - diff
            # Adjust orb if retrograde
            active_orb = orb
            if positions[p_name].retrograde:
                if p_name == "Mercury":
                    active_orb = 12.0
                elif p_name == "Venus":
                    active_orb = 8.0
            if diff <= active_orb:
                positions[p_name].is_combust = True

    return positions

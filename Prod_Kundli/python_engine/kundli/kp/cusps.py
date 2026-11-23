"""KP Cusps and Planetary Table with 4-fold hierarchy."""
from typing import Dict, Any, List
from pydantic import BaseModel
from kundli.kp.sublords import get_kp_sub_lord
from kundli.astronomy.houses import HouseCusp
from kundli.astronomy.planets import PlanetPosition


class KPCuspDetail(BaseModel):
    house: int
    longitude: float
    sign: str
    sign_lord: str
    star: str
    star_lord: str
    sub_lord: str
    sub_sub_lord: str
    degree_in_sign: float


class KPPlanetDetail(BaseModel):
    planet: str
    longitude: float
    sign: str
    sign_lord: str
    star: str
    star_lord: str
    sub_lord: str
    sub_sub_lord: str
    degree_in_sign: float
    house: int
    retrograde: bool


def calculate_kp_cusp_table(house_cusps: List[HouseCusp]) -> List[KPCuspDetail]:
    """Generate the KP 12 Cuspal Positions with Sign, Star, Sub, Sub-sub lords."""
    kp_cusps = []
    for h in house_cusps:
        sub_info = get_kp_sub_lord(h.longitude)
        kp_cusps.append(KPCuspDetail(
            house=h.house,
            longitude=h.longitude,
            sign=sub_info["sign"],
            sign_lord=sub_info["sign_lord"],
            star=sub_info["star"],
            star_lord=sub_info["star_lord"],
            sub_lord=sub_info["sub_lord"],
            sub_sub_lord=sub_info["sub_sub_lord"],
            degree_in_sign=sub_info["degree_in_sign"]
        ))
    return kp_cusps


def calculate_kp_planet_table(planets: Dict[str, PlanetPosition]) -> List[KPPlanetDetail]:
    """Generate the KP Planetary Table with Sign, Star, Sub, Sub-sub lords."""
    kp_planets = []
    for p_name, p in planets.items():
        sub_info = get_kp_sub_lord(p.longitude)
        kp_planets.append(KPPlanetDetail(
            planet=p_name,
            longitude=p.longitude,
            sign=sub_info["sign"],
            sign_lord=sub_info["sign_lord"],
            star=sub_info["star"],
            star_lord=sub_info["star_lord"],
            sub_lord=sub_info["sub_lord"],
            sub_sub_lord=sub_info["sub_sub_lord"],
            degree_in_sign=sub_info["degree_in_sign"],
            house=p.bhava_chalit_house,
            retrograde=p.retrograde
        ))
    return kp_planets

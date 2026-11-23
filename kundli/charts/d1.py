"""Janma Rashi (D1), Chandra (Moon), Surya (Sun), and Bhava Chalit chart representations."""
from typing import Dict, Any, List
from kundli.core.zodiac import ZODIAC_SIGNS, SIGN_LORDS
from kundli.astronomy.planets import PlanetPosition


def build_rashi_chart(
    ascendant: PlanetPosition,
    planets: Dict[str, PlanetPosition]
) -> Dict[str, Any]:
    """Generate Janma Kundli (D1) structure."""
    asc_idx = ascendant.sign_index
    house_planets: Dict[int, List[Dict[str, Any]]] = {h: [] for h in range(1, 13)}
    house_signs: Dict[int, str] = {}

    for h in range(1, 13):
        s_idx = (asc_idx + h - 1) % 12
        house_signs[h] = ZODIAC_SIGNS[s_idx]

    for p_name, p in planets.items():
        house_planets[p.house].append({
            "planet": p_name,
            "sign": p.sign,
            "degree": p.degree_in_sign,
            "retrograde": p.retrograde,
            "is_combust": p.is_combust
        })

    return {
        "chart_type": "D1 Janma Kundli",
        "ascendant_sign": ascendant.sign,
        "ascendant_degree": ascendant.degree_in_sign,
        "house_signs": house_signs,
        "house_planets": house_planets
    }


def build_chandra_kundli(
    planets: Dict[str, PlanetPosition]
) -> Dict[str, Any]:
    """Generate Chandra Kundli (Moon chart: Moon sign is House 1)."""
    moon = planets["Moon"]
    moon_idx = moon.sign_index
    house_planets: Dict[int, List[str]] = {h: [] for h in range(1, 13)}
    house_signs: Dict[int, str] = {}

    for h in range(1, 13):
        s_idx = (moon_idx + h - 1) % 12
        house_signs[h] = ZODIAC_SIGNS[s_idx]

    for p_name, p in planets.items():
        chandra_house = ((p.sign_index - moon_idx) % 12) + 1
        house_planets[chandra_house].append(p_name)

    return {
        "chart_type": "Chandra Kundli",
        "moon_sign": moon.sign,
        "moon_degree": moon.degree_in_sign,
        "house_signs": house_signs,
        "house_planets": house_planets
    }


def build_surya_kundli(
    planets: Dict[str, PlanetPosition]
) -> Dict[str, Any]:
    """Generate Surya Kundli (Sun chart: Sun sign is House 1)."""
    sun = planets["Sun"]
    sun_idx = sun.sign_index
    house_planets: Dict[int, List[str]] = {h: [] for h in range(1, 13)}
    house_signs: Dict[int, str] = {}

    for h in range(1, 13):
        s_idx = (sun_idx + h - 1) % 12
        house_signs[h] = ZODIAC_SIGNS[s_idx]

    for p_name, p in planets.items():
        surya_house = ((p.sign_index - sun_idx) % 12) + 1
        house_planets[surya_house].append(p_name)

    return {
        "chart_type": "Surya Kundli",
        "sun_sign": sun.sign,
        "sun_degree": sun.degree_in_sign,
        "house_signs": house_signs,
        "house_planets": house_planets
    }

"""KP 4-Step Significators and House Significations."""
from typing import Dict, Any, List, Set
from pydantic import BaseModel
from kundli.kp.cusps import KPCuspDetail, KPPlanetDetail


class KPPlanetSignification(BaseModel):
    planet: str
    level_1: List[int]  # Houses occupied by Star Lord
    level_2: List[int]  # House occupied by the planet itself
    level_3: List[int]  # Houses owned by Star Lord
    level_4: List[int]  # Houses owned by the planet itself
    all_signified_houses: List[int]


class KPHouseSignification(BaseModel):
    house: int
    significators_level_1: List[str]  # Planets in star of occupant
    significators_level_2: List[str]  # Occupants of the house
    significators_level_3: List[str]  # Planets in star of house lord
    significators_level_4: List[str]  # House lord
    all_significators: List[str]


def calculate_kp_significators(
    kp_planets: List[KPPlanetDetail],
    kp_cusps: List[KPCuspDetail]
) -> Dict[str, Any]:
    """Calculate 4-step KP significators for planets and houses.
    Level 1: Planets in the star of occupants of the house (Strongest)
    Level 2: Occupant of the house
    Level 3: Planets in the star of the lord of the house
    Level 4: Lord of the house
    """
    # 1. Map houses to occupants
    house_occupants: Dict[int, List[str]] = {i: [] for i in range(1, 13)}
    planet_house_map: Dict[str, int] = {}
    planet_star_map: Dict[str, str] = {}
    
    for p in kp_planets:
        house_occupants[p.house].append(p.planet)
        planet_house_map[p.planet] = p.house
        planet_star_map[p.planet] = p.star_lord

    # 2. Map houses to owner (cusp sign lord)
    house_lord_map: Dict[int, str] = {}
    lord_houses_map: Dict[str, List[int]] = {}
    for c in kp_cusps:
        house_lord_map[c.house] = c.sign_lord
        lord_houses_map.setdefault(c.sign_lord, []).append(c.house)

    # 3. Compute Planet-centric significations
    planet_significations: List[KPPlanetSignification] = []
    for p in kp_planets:
        star_lord = p.star_lord
        
        # Level 1: House occupied by star lord
        l1 = [planet_house_map[star_lord]] if star_lord in planet_house_map else []
        # Level 2: House occupied by planet
        l2 = [p.house]
        # Level 3: Houses owned by star lord
        l3 = lord_houses_map.get(star_lord, [])
        # Level 4: Houses owned by planet
        l4 = lord_houses_map.get(p.planet, [])

        combined: Set[int] = set(l1 + l2 + l3 + l4)
        planet_significations.append(KPPlanetSignification(
            planet=p.planet,
            level_1=sorted(l1),
            level_2=sorted(l2),
            level_3=sorted(l3),
            level_4=sorted(l4),
            all_signified_houses=sorted(list(combined))
        ))

    # 4. Compute House-centric significations
    house_significations: List[KPHouseSignification] = []
    for h in range(1, 13):
        occupants = house_occupants.get(h, [])
        h_lord = house_lord_map.get(h, "")

        # Level 1: Planets whose star lord is an occupant of house h
        l1_planets = [p.planet for p in kp_planets if p.star_lord in occupants]
        # Level 2: Occupants of house h
        l2_planets = occupants
        # Level 3: Planets whose star lord is the lord of house h
        l3_planets = [p.planet for p in kp_planets if p.star_lord == h_lord]
        # Level 4: Lord of house h
        l4_planets = [h_lord] if h_lord else []

        all_sig: Set[str] = set(l1_planets + l2_planets + l3_planets + l4_planets)
        house_significations.append(KPHouseSignification(
            house=h,
            significators_level_1=sorted(l1_planets),
            significators_level_2=sorted(l2_planets),
            significators_level_3=sorted(l3_planets),
            significators_level_4=sorted(l4_planets),
            all_significators=sorted(list(all_sig))
        ))

    return {
        "planet_significators": planet_significations,
        "house_significators": house_significations
    }

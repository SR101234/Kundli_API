"""House lordship classifications: Kendras, Trikonas, Dusthanas, Upachayas, Marakas."""
from typing import Dict, Any, List
from kundli.core.zodiac import ZODIAC_SIGNS, SIGN_LORDS

# Standard functional house types
KENDRAS = [1, 4, 7, 10]
TRIKONAS = [1, 5, 9]
DUSTHANAS = [6, 8, 12]
UPACHAYAS = [3, 6, 10, 11]
MARAKAS = [2, 7]


def get_house_lords(ascendant_sign_index: int) -> Dict[int, Dict[str, Any]]:
    """Determine the sign and lord of each of the 12 houses from Ascendant sign."""
    house_details = {}
    for h in range(1, 13):
        sign_idx = (ascendant_sign_index + h - 1) % 12
        sign_name = ZODIAC_SIGNS[sign_idx]
        lord = SIGN_LORDS[sign_name]
        house_details[h] = {
            "house": h,
            "sign": sign_name,
            "sign_index": sign_idx,
            "lord": lord,
            "is_kendra": h in KENDRAS,
            "is_trikona": h in TRIKONAS,
            "is_dusthana": h in DUSTHANAS,
            "is_upachaya": h in UPACHAYAS,
            "is_maraka": h in MARAKAS
        }
    return house_details


def get_planets_in_houses(planets: Dict[str, Any]) -> Dict[int, List[str]]:
    """Map house number (1-12) to list of planets present in that house."""
    h_map: Dict[int, List[str]] = {i: [] for i in range(1, 13)}
    for p_name, p in planets.items():
        if p.house in h_map:
            h_map[p.house].append(p_name)
    return h_map

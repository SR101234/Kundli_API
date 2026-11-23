"""KP Ruling Planets (RP) determination."""
from typing import Dict, Any, List
from kundli.kp.sublords import get_kp_sub_lord
from kundli.astronomy.planets import PlanetPosition


def calculate_ruling_planets(
    day_lord: str,
    moon_lon: float,
    asc_lon: float,
    rahu_lon: float,
    ketu_lon: float
) -> Dict[str, Any]:
    """Calculate the 5 primary Ruling Planets (RP) used in KP astrology."""
    moon_kp = get_kp_sub_lord(moon_lon)
    asc_kp = get_kp_sub_lord(asc_lon)

    # 5 standard ruling planets
    ruling_order = [
        {"role": "Ascendant Sub Lord", "planet": asc_kp["sub_lord"]},
        {"role": "Ascendant Star Lord", "planet": asc_kp["star_lord"]},
        {"role": "Ascendant Sign Lord", "planet": asc_kp["sign_lord"]},
        {"role": "Moon Star Lord", "planet": moon_kp["star_lord"]},
        {"role": "Moon Sign Lord", "planet": moon_kp["sign_lord"]},
        {"role": "Day Lord", "planet": day_lord}
    ]

    # Node representations
    rahu_kp = get_kp_sub_lord(rahu_lon)
    ketu_kp = get_kp_sub_lord(ketu_lon)

    node_conjunctions = {
        "Rahu_represents": [rahu_kp["sign_lord"], rahu_kp["star_lord"]],
        "Ketu_represents": [ketu_kp["sign_lord"], ketu_kp["star_lord"]]
    }

    return {
        "primary_ruling_planets": ruling_order,
        "node_affiliations": node_conjunctions
    }

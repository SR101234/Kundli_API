"""Planetary dignity, exaltation, debilitation, moolatrikona, and Panchadha Maitri."""
from typing import Dict, Any, List
from kundli.core.zodiac import ZODIAC_SIGNS, SIGN_LORDS

# Deep exaltation and debilitation degrees
EXALTATION_DATA = {
    "Sun": {"sign": "Aries", "deep_deg": 10.0, "deb_sign": "Libra"},
    "Moon": {"sign": "Taurus", "deep_deg": 3.0, "deb_sign": "Scorpio"},
    "Mars": {"sign": "Capricorn", "deep_deg": 28.0, "deb_sign": "Cancer"},
    "Mercury": {"sign": "Virgo", "deep_deg": 15.0, "deb_sign": "Pisces"},
    "Jupiter": {"sign": "Cancer", "deep_deg": 5.0, "deb_sign": "Capricorn"},
    "Venus": {"sign": "Pisces", "deep_deg": 27.0, "deb_sign": "Virgo"},
    "Saturn": {"sign": "Libra", "deep_deg": 20.0, "deb_sign": "Aries"},
    "Rahu": {"sign": "Taurus", "deep_deg": 15.0, "deb_sign": "Scorpio"},
    "Ketu": {"sign": "Scorpio", "deep_deg": 15.0, "deb_sign": "Taurus"},
}

MOOLATRIKONA_RANGES = {
    "Sun": {"sign": "Leo", "start": 0.0, "end": 20.0},
    "Moon": {"sign": "Taurus", "start": 3.0, "end": 30.0},
    "Mars": {"sign": "Aries", "start": 0.0, "end": 12.0},
    "Mercury": {"sign": "Virgo", "start": 15.0, "end": 20.0},
    "Jupiter": {"sign": "Sagittarius", "start": 0.0, "end": 10.0},
    "Venus": {"sign": "Libra", "start": 0.0, "end": 15.0},
    "Saturn": {"sign": "Aquarius", "start": 0.0, "end": 20.0},
}

# Naisargika (Natural) relationships per Parashara
NATURAL_RELATIONSHIPS = {
    "Sun": {
        "friends": ["Moon", "Mars", "Jupiter"],
        "neutrals": ["Mercury"],
        "enemies": ["Venus", "Saturn", "Rahu", "Ketu"]
    },
    "Moon": {
        "friends": ["Sun", "Mercury"],
        "neutrals": ["Mars", "Jupiter", "Venus", "Saturn"],
        "enemies": ["Rahu", "Ketu"]
    },
    "Mars": {
        "friends": ["Sun", "Moon", "Jupiter"],
        "neutrals": ["Venus", "Saturn"],
        "enemies": ["Mercury", "Rahu"]
    },
    "Mercury": {
        "friends": ["Sun", "Venus"],
        "neutrals": ["Mars", "Jupiter", "Saturn"],
        "enemies": ["Moon"]
    },
    "Jupiter": {
        "friends": ["Sun", "Moon", "Mars"],
        "neutrals": ["Saturn"],
        "enemies": ["Mercury", "Venus"]
    },
    "Venus": {
        "friends": ["Mercury", "Saturn", "Rahu", "Ketu"],
        "neutrals": ["Mars", "Jupiter"],
        "enemies": ["Sun", "Moon"]
    },
    "Saturn": {
        "friends": ["Mercury", "Venus", "Rahu"],
        "neutrals": ["Jupiter"],
        "enemies": ["Sun", "Moon", "Mars", "Ketu"]
    },
    "Rahu": {
        "friends": ["Venus", "Saturn", "Mercury"],
        "neutrals": ["Jupiter"],
        "enemies": ["Sun", "Moon", "Mars"]
    },
    "Ketu": {
        "friends": ["Mars", "Venus", "Saturn"],
        "neutrals": ["Jupiter", "Mercury"],
        "enemies": ["Sun", "Moon"]
    }
}


def calculate_temporal_relationship(planet_house: int, target_house: int) -> str:
    """Planets in 2nd, 3rd, 4th, 10th, 11th, 12th from a planet are temporary friends; others enemies."""
    diff = (target_house - planet_house) % 12
    if diff in (1, 2, 3, 9, 10, 11):  # 2nd, 3rd, 4th, 10th, 11th, 12th
        return "friend"
    return "enemy"


def calculate_compound_relationship(natural: str, temporal: str) -> str:
    """Panchadha Maitri: combines natural and temporal relationships."""
    if natural == "friend" and temporal == "friend":
        return "Great Friend"
    elif natural == "friend" and temporal == "enemy":
        return "Neutral"
    elif natural == "neutral" and temporal == "friend":
        return "Friend"
    elif natural == "neutral" and temporal == "enemy":
        return "Enemy"
    elif natural == "enemy" and temporal == "friend":
        return "Neutral"
    elif natural == "enemy" and temporal == "enemy":
        return "Great Enemy"
    return "Neutral"


def get_planet_dignity(
    planet_name: str,
    sign: str,
    degree_in_sign: float,
    planet_house: int,
    house_planets: Dict[str, int]
) -> Dict[str, Any]:
    """Calculate exact dignity: Exalted, Debilitated, Moolatrikona, Own Sign, or compound relationship."""
    if planet_name not in EXALTATION_DATA:
        return {"dignity": "Neutral", "score": 50, "is_debilitated": False, "is_exalted": False}

    exalt = EXALTATION_DATA[planet_name]
    sign_lord = SIGN_LORDS[sign]

    if sign == exalt["sign"]:
        return {
            "dignity": "Exalted",
            "score": 100,
            "is_exalted": True,
            "is_debilitated": False,
            "deep_degree": exalt["deep_deg"],
            "difference": round(abs(degree_in_sign - exalt["deep_deg"]), 2)
        }
    if sign == exalt["deb_sign"]:
        return {
            "dignity": "Debilitated",
            "score": 10,
            "is_exalted": False,
            "is_debilitated": True,
            "deep_degree": exalt["deep_deg"],
            "difference": round(abs(degree_in_sign - exalt["deep_deg"]), 2)
        }

    # Check Moolatrikona
    if planet_name in MOOLATRIKONA_RANGES:
        mt = MOOLATRIKONA_RANGES[planet_name]
        if sign == mt["sign"] and mt["start"] <= degree_in_sign <= mt["end"]:
            return {"dignity": "Moolatrikona", "score": 90, "is_exalted": False, "is_debilitated": False}

    # Check Own Sign
    if sign_lord == planet_name:
        return {"dignity": "Own Sign", "score": 80, "is_exalted": False, "is_debilitated": False}

    # Compound relationship with sign lord
    nat_dict = NATURAL_RELATIONSHIPS.get(planet_name, {"friends": [], "neutrals": [], "enemies": []})
    if sign_lord in nat_dict["friends"]:
        nat_rel = "friend"
    elif sign_lord in nat_dict["enemies"]:
        nat_rel = "enemy"
    else:
        nat_rel = "neutral"

    # Temporal relationship
    sign_lord_house = house_planets.get(sign_lord, planet_house)
    temp_rel = calculate_temporal_relationship(planet_house, sign_lord_house)
    compound = calculate_compound_relationship(nat_rel, temp_rel)

    score_map = {
        "Great Friend": 70,
        "Friend": 60,
        "Neutral": 50,
        "Enemy": 30,
        "Great Enemy": 20
    }

    return {
        "dignity": compound,
        "score": score_map.get(compound, 50),
        "is_exalted": False,
        "is_debilitated": False,
        "sign_lord": sign_lord,
        "natural_relation": nat_rel,
        "temporal_relation": temp_rel
    }

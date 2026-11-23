"""Vedic Drishti / Aspects calculation engine."""
from typing import Dict, Any, List

# Special aspects in Vedic Astrology (in houses from planet)
# All planets aspect 7th house with full drishti.
# Mars aspects 4th, 7th, 8th.
# Jupiter aspects 5th, 7th, 9th.
# Saturn aspects 3rd, 7th, 10th.
# Rahu/Ketu aspect 5th, 7th, 9th.
SPECIAL_ASPECTS: Dict[str, List[int]] = {
    "Sun": [7],
    "Moon": [7],
    "Mars": [4, 7, 8],
    "Mercury": [7],
    "Jupiter": [5, 7, 9],
    "Venus": [7],
    "Saturn": [3, 7, 10],
    "Rahu": [5, 7, 9],
    "Ketu": [5, 7, 9],
}


def calculate_aspected_houses(planet_name: str, planet_house: int) -> List[int]:
    """Return the list of houses aspected by this planet (1-12)."""
    aspect_offsets = SPECIAL_ASPECTS.get(planet_name, [7])
    aspected = []
    for off in aspect_offsets:
        h = ((planet_house - 1 + off - 1) % 12) + 1
        aspected.append(h)
    return aspected


def calculate_mutual_aspects(planet_positions: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Determine which planets aspect each other."""
    aspects = []
    names = [p for p in planet_positions.keys() if p in SPECIAL_ASPECTS]
    
    for i in range(len(names)):
        p1 = names[i]
        h1 = planet_positions[p1].house
        aspected_by_p1 = calculate_aspected_houses(p1, h1)

        for j in range(len(names)):
            if i == j:
                continue
            p2 = names[j]
            h2 = planet_positions[p2].house
            if h2 in aspected_by_p1:
                # p1 aspects p2
                aspected_by_p2 = calculate_aspected_houses(p2, h2)
                is_mutual = h1 in aspected_by_p2
                aspects.append({
                    "aspector": p1,
                    "aspected": p2,
                    "aspector_house": h1,
                    "aspected_house": h2,
                    "is_mutual": is_mutual
                })
    return aspects

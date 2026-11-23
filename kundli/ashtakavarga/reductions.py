"""Trikona Shodhana, Ekadhipatya Shodhana, and Shodhya Pinda calculations."""
from typing import Dict, Any, List

# Rashi multipliers (Rashi Pinda)
RASHI_MULTIPLIERS = [7, 10, 8, 4, 10, 5, 7, 8, 9, 5, 11, 12]  # Aries=7 ... Pisces=12
# Graha multipliers (Graha Pinda)
PLANET_MULTIPLIERS = {
    "Sun": 5, "Moon": 5, "Mars": 8, "Mercury": 5,
    "Jupiter": 10, "Venus": 7, "Saturn": 5
}

# Trikona (triplicity) sign triads
TRIKONA_GROUPS = [
    [0, 4, 8],   # Aries, Leo, Sagittarius (Fire)
    [1, 5, 9],   # Taurus, Virgo, Capricorn (Earth)
    [2, 6, 10],  # Gemini, Libra, Aquarius (Air)
    [3, 7, 11]   # Cancer, Scorpio, Pisces (Water)
]

# Dual ownership pairs for Ekadhipatya Shodhana:
# Mars (Aries 0, Scorpio 7)
# Venus (Taurus 1, Libra 6)
# Mercury (Gemini 2, Virgo 5)
# Jupiter (Sagittarius 8, Pisces 11)
# Saturn (Capricorn 9, Aquarius 10)
# (Sun=4 Leo and Moon=3 Cancer have single signs, exempt from Ekadhipatya reduction)
DUAL_PAIRS = [(0, 7), (1, 6), (2, 5), (8, 11), (9, 10)]


def trikona_shodhana(bindus: List[int]) -> List[int]:
    """Trikona reduction: subtract the minimum value in each trine group."""
    reduced = list(bindus)
    for group in TRIKONA_GROUPS:
        min_val = min(reduced[group[0]], reduced[group[1]], reduced[group[2]])
        for idx in group:
            reduced[idx] -= min_val
    return reduced


def ekadhipatya_shodhana(reduced_bindus: List[int], planet_sign_indices: Dict[str, int]) -> List[int]:
    """Ekadhipatya reduction for signs owned by the same planet."""
    final_bindus = list(reduced_bindus)

    # Planets present in each sign
    planets_in_sign = {i: [] for i in range(12)}
    for p, s in planet_sign_indices.items():
        if p in ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"):
            planets_in_sign[s].append(p)

    for s1, s2 in DUAL_PAIRS:
        v1 = final_bindus[s1]
        v2 = final_bindus[s2]
        p1 = len(planets_in_sign[s1]) > 0
        p2 = len(planets_in_sign[s2]) > 0

        if v1 == 0 or v2 == 0:
            continue
        if p1 and p2:
            # Both occupied: no reduction
            continue
        elif not p1 and not p2:
            # Neither occupied: reduce larger to equal the smaller, or if equal make both 0
            if v1 == v2:
                final_bindus[s1] = 0
                final_bindus[s2] = 0
            elif v1 > v2:
                final_bindus[s1] = v2
            else:
                final_bindus[s2] = v1
        elif p1 and not p2:
            # s1 occupied, s2 unoccupied: reduce s2
            final_bindus[s2] = 0
        elif not p1 and p2:
            # s1 unoccupied, s2 occupied: reduce s1
            final_bindus[s1] = 0

    return final_bindus


def calculate_shodhya_pinda(
    final_bindus: List[int],
    planet_sign_indices: Dict[str, int]
) -> Dict[str, int]:
    """Calculate Rashi Pinda, Graha Pinda, and Shodhya Pinda (sum)."""
    # Rashi Pinda
    rashi_pinda = sum(final_bindus[i] * RASHI_MULTIPLIERS[i] for i in range(12))

    # Graha Pinda
    graha_pinda = 0
    for p_name, mult in PLANET_MULTIPLIERS.items():
        if p_name in planet_sign_indices:
            s_idx = planet_sign_indices[p_name]
            graha_pinda += final_bindus[s_idx] * mult

    return {
        "rashi_pinda": rashi_pinda,
        "graha_pinda": graha_pinda,
        "shodhya_pinda": rashi_pinda + graha_pinda
    }

"""Shadbala (Six-fold planetary strength) calculation framework."""
from typing import Dict, Any, List
from pydantic import BaseModel
from kundli.core.zodiac import ZODIAC_SIGNS
from kundli.core.dignity import EXALTATION_DATA

# Minimum required Shadbala in Rupas (60 Virupas = 1 Rupa)
MINIMUM_SHADBALA_RUPAS = {
    "Sun": 6.5,     # 390 Virupas
    "Moon": 6.0,    # 360 Virupas
    "Mars": 5.0,    # 300 Virupas
    "Mercury": 7.0, # 420 Virupas
    "Jupiter": 6.5, # 390 Virupas
    "Venus": 5.5,   # 330 Virupas
    "Saturn": 5.0,  # 300 Virupas
}

# Naisargika (Natural) Bala in Virupas (Brihat Parashara Hora Shastra)
NAISARGIKA_BALA_VIRUPAS = {
    "Sun": 60.0,
    "Moon": 51.43,
    "Venus": 42.86,
    "Jupiter": 34.29,
    "Mercury": 25.71,
    "Mars": 17.14,
    "Saturn": 8.57
}

# Directional (Dig Bala) strongest house:
# 1st: Jupiter & Mercury; 4th: Moon & Venus; 7th: Saturn; 10th: Sun & Mars
DIG_BALA_HOUSES = {
    "Jupiter": 1, "Mercury": 1,
    "Moon": 4, "Venus": 4,
    "Saturn": 7,
    "Sun": 10, "Mars": 10
}


def calculate_shadbala(
    planets: Dict[str, Any],
    ascendant_longitude: float
) -> Dict[str, Any]:
    """Calculate Shadbala (six-fold strength) in Rupas and Virupas for the 7 traditional planets."""
    shadbala_results = []

    for p_name in ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"):
        p = planets[p_name]
        p_lon = p.longitude
        exalt_info = EXALTATION_DATA[p_name]

        # 1. Uchcha Bala (Exaltation strength, max 60 Virupas)
        # Distance from deep debilitation point
        deb_sign_idx = ZODIAC_SIGNS.index(exalt_info["deb_sign"])
        deb_deg = deb_sign_idx * 30.0 + exalt_info["deep_deg"]
        diff_deb = abs(p_lon - deb_deg) % 360.0
        if diff_deb > 180.0:
            diff_deb = 360.0 - diff_deb
        uchcha_bala = round((diff_deb / 180.0) * 60.0, 2)

        # 2. Dig Bala (Directional strength, max 60 Virupas)
        ideal_house = DIG_BALA_HOUSES[p_name]
        h_diff = abs(p.house - ideal_house)
        if h_diff > 6:
            h_diff = 12 - h_diff
        dig_bala = round((1.0 - (h_diff / 6.0)) * 60.0, 2)

        # 3. Naisargika Bala (Natural strength)
        naisargika_bala = NAISARGIKA_BALA_VIRUPAS[p_name]

        # 4. Cheshta Bala (Motional strength, retrograde gets maximum 60 virupas)
        if p_name in ("Sun", "Moon"):
            # Ayana bala proxy for luminaries
            cheshta_bala = 35.0
        else:
            cheshta_bala = 60.0 if p.retrograde else (30.0 + min(abs(p.speed) * 15.0, 25.0))
        cheshta_bala = round(cheshta_bala, 2)

        # 5. Sthana Bala component proxy (Kendra, Moolatrikona, etc.)
        kendra_bonus = 60.0 if p.house in (1, 4, 7, 10) else (30.0 if p.house in (2, 5, 8, 11) else 15.0)
        sthana_bala = round(uchcha_bala + kendra_bonus, 2)

        # 6. Kala Bala (Time/Paksha/Day component proxy)
        kala_bala = 45.0

        # Total Virupas and Rupas
        total_virupas = round(sthana_bala + dig_bala + kala_bala + cheshta_bala + naisargika_bala, 2)
        total_rupas = round(total_virupas / 60.0, 2)
        min_required = MINIMUM_SHADBALA_RUPAS[p_name]
        is_strong = total_rupas >= min_required
        ratio = round((total_rupas / min_required) * 100, 1)

        shadbala_results.append({
            "planet": p_name,
            "total_virupas": total_virupas,
            "total_rupas": total_rupas,
            "required_rupas": min_required,
            "strength_percentage": ratio,
            "is_sufficient": is_strong,
            "status": "Strong" if is_strong else "Deficient",
            "breakdown": {
                "sthana_bala": sthana_bala,
                "dig_bala": dig_bala,
                "kala_bala": kala_bala,
                "cheshta_bala": cheshta_bala,
                "naisargika_bala": naisargika_bala,
                "uchcha_bala": uchcha_bala
            }
        })

    return {
        "shadbala_table": shadbala_results
    }

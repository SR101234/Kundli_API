"""KP Astrology (Krishnamurti Paddhati) Sub-Lord and Sub-Sub-Lord calculation."""
from typing import Dict, Any, List, Tuple
from kundli.core.zodiac import get_sign_from_longitude
from kundli.core.nakshatra import get_nakshatra_from_longitude, NAKSHATRA_LORDS

# Vimshottari Dasha planetary sequence and years (total 120 years)
VIMSHOTTARI_LORDS = [
    ("Ketu", 7),
    ("Venus", 20),
    ("Sun", 6),
    ("Moon", 10),
    ("Mars", 7),
    ("Rahu", 18),
    ("Jupiter", 16),
    ("Saturn", 19),
    ("Mercury", 17)
]
VIMSHOTTARI_CYCLE = [p[0] for p in VIMSHOTTARI_LORDS]
VIMSHOTTARI_YEARS = {p[0]: p[1] for p in VIMSHOTTARI_LORDS}
TOTAL_VIM_YEARS = 120.0


def get_kp_sub_lord(longitude: float) -> Dict[str, Any]:
    """Calculate Sign Lord, Star Lord, Sub Lord, and Sub-Sub Lord for any longitude."""
    lon = longitude % 360.0
    sign_info = get_sign_from_longitude(lon)
    nak_info = get_nakshatra_from_longitude(lon)

    star_lord = nak_info["nakshatra_lord"]
    deg_in_nak = nak_info["degree_in_nakshatra"]  # 0 to 13.333333 degrees

    # Starting index in Vimshottari sequence for this star lord
    start_idx = VIMSHOTTARI_CYCLE.index(star_lord)
    
    nak_span_deg = 360.0 / 27.0  # 13.333333333333334 degrees
    cum_deg = 0.0
    sub_lord = star_lord
    sub_sub_lord = star_lord
    deg_in_sub = 0.0
    sub_span = 0.0

    # Determine Sub-Lord
    for i in range(9):
        p_name = VIMSHOTTARI_CYCLE[(start_idx + i) % 9]
        p_years = VIMSHOTTARI_YEARS[p_name]
        p_sub_span = nak_span_deg * (p_years / TOTAL_VIM_YEARS)

        if cum_deg <= deg_in_nak < cum_deg + p_sub_span or i == 8:
            sub_lord = p_name
            deg_in_sub = deg_in_nak - cum_deg
            sub_span = p_sub_span
            break
        cum_deg += p_sub_span

    # Determine Sub-Sub-Lord within the Sub-Lord
    sub_start_idx = VIMSHOTTARI_CYCLE.index(sub_lord)
    cum_sub_deg = 0.0
    for j in range(9):
        p_ss_name = VIMSHOTTARI_CYCLE[(sub_start_idx + j) % 9]
        p_ss_years = VIMSHOTTARI_YEARS[p_ss_name]
        p_ss_span = sub_span * (p_ss_years / TOTAL_VIM_YEARS)

        if cum_sub_deg <= deg_in_sub < cum_sub_deg + p_ss_span or j == 8:
            sub_sub_lord = p_ss_name
            break
        cum_sub_deg += p_ss_span

    return {
        "longitude": round(lon, 4),
        "sign": sign_info["sign"],
        "sign_lord": sign_info["sign_lord"],
        "star": nak_info["nakshatra"],
        "star_lord": star_lord,
        "sub_lord": sub_lord,
        "sub_sub_lord": sub_sub_lord,
        "nakshatra_pada": nak_info["nakshatra_pada"],
        "degree_in_sign": round(sign_info["degree_in_sign"], 4)
    }

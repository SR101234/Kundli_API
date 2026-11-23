"""Kakshya divisions for Ashtakavarga transit analysis."""
from typing import Dict, Any, List

# Each 30-degree sign is divided into 8 equal Kakshyas of 3°45' (3.75°).
# Kakshya lords order: Saturn, Jupiter, Mars, Sun, Venus, Mercury, Moon, Lagna
KAKSHYA_LORDS = ["Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury", "Moon", "Ascendant"]


def get_kakshya_details(longitude: float) -> Dict[str, Any]:
    """Return which Kakshya (1 to 8) and which lord governs the given longitude."""
    deg_in_sign = longitude % 30.0
    k_idx = int(deg_in_sign // 3.75)
    k_idx = min(k_idx, 7)
    return {
        "kakshya_number": k_idx + 1,
        "kakshya_lord": KAKSHYA_LORDS[k_idx],
        "degree_start": k_idx * 3.75,
        "degree_end": (k_idx + 1) * 3.75
    }

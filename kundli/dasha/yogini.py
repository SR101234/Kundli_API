"""Yogini Dasha calculation engine (36-year cycle)."""
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from kundli.core.nakshatra import get_nakshatra_from_longitude

# 8 Yoginis, ruling planets, and span of years (total 36 years)
YOGINIS = [
    {"name": "Mangla", "lord": "Moon", "years": 1},
    {"name": "Pingla", "lord": "Sun", "years": 2},
    {"name": "Dhanya", "lord": "Jupiter", "years": 3},
    {"name": "Bhramari", "lord": "Mars", "years": 4},
    {"name": "Bhadrika", "lord": "Mercury", "years": 5},
    {"name": "Ulka", "lord": "Saturn", "years": 6},
    {"name": "Siddha", "lord": "Venus", "years": 7},
    {"name": "Sankata", "lord": "Rahu", "years": 8},
]
TOTAL_YOGINI_YEARS = 36.0


def calculate_yogini_dasha(
    birth_datetime: datetime,
    moon_longitude: float,
    cycles: int = 2
) -> Dict[str, Any]:
    """Calculate Yogini Dasha timeline.
    Starting Yogini rule: (Nakshatra number + 3) % 8.
    """
    moon_nak = get_nakshatra_from_longitude(moon_longitude)
    nak_num = moon_nak["nakshatra_number"]  # 1 to 27
    deg_in_nak = moon_nak["degree_in_nakshatra"]
    nak_span = 360.0 / 27.0

    starting_yogini_idx = (nak_num + 3) % 8
    starting_yogini = YOGINIS[starting_yogini_idx]

    # Balance of initial Yogini
    balance_frac = 1.0 - (deg_in_nak / nak_span)
    initial_years = starting_yogini["years"] * balance_frac

    timeline = []
    current_start = birth_datetime

    # Generate cycles
    for c in range(cycles):
        for i in range(8):
            y_idx = (starting_yogini_idx + i) % 8
            y_info = YOGINIS[y_idx]
            duration_y = initial_years if (c == 0 and i == 0) else y_info["years"]
            cur_end = current_start + timedelta(days=duration_y * 365.2422)

            timeline.append({
                "yogini": y_info["name"],
                "lord": y_info["lord"],
                "years": round(duration_y, 2),
                "start_date": current_start.strftime("%Y-%m-%d"),
                "end_date": cur_end.strftime("%Y-%m-%d")
            })
            current_start = cur_end

    return {
        "system": "Yogini Dasha (36-year cycle)",
        "starting_yogini": starting_yogini["name"],
        "starting_lord": starting_yogini["lord"],
        "balance_years": round(initial_years, 2),
        "periods": timeline
    }

"""Saturn Sade Sati and Dhaiya (Kantaka / Ashtama Shani) detection."""
from datetime import datetime
from typing import Dict, Any, List
from kundli.astronomy.ephemeris import calculate_julian_day
from kundli.astronomy.planets import calculate_planet_positions


def evaluate_sade_sati(
    natal_moon_sign_idx: int,
    saturn_transit_sign_idx: int
) -> Dict[str, Any]:
    """Detect whether native is currently undergoing Shani Sade Sati or Dhaiya.
    Sade Sati covers:
    - 12th from Moon: Phase 1 (Rising / Aardha)
    - 1st from Moon: Phase 2 (Peak / Madhyama)
    - 2nd from Moon: Phase 3 (Setting / Antya)
    Dhaiya covers:
    - 4th from Moon: Kantaka Shani / Ardhashtama Shani
    - 8th from Moon: Ashtama Shani
    """
    house_from_moon = ((saturn_transit_sign_idx - natal_moon_sign_idx) % 12) + 1

    is_sade_sati = False
    phase_name = "None"
    description = "Saturn is not currently transiting over the natal Moon zone."
    severity = "none"

    if house_from_moon == 12:
        is_sade_sati = True
        phase_name = "Phase 1: Rising Phase (Aardha Sade Sati)"
        description = "Saturn is transiting the 12th house from natal Moon. Represents mental realignment, unexpected travels, and discipline in financial expenditures."
        severity = "moderate"
    elif house_from_moon == 1:
        is_sade_sati = True
        phase_name = "Phase 2: Peak Phase (Janma Shani)"
        description = "Saturn is transiting directly over the natal Moon. Intensely transformational, demanding integrity, mental resilience, and heavy work ethic."
        severity = "high"
    elif house_from_moon == 2:
        is_sade_sati = True
        phase_name = "Phase 3: Setting Phase (Antya Sade Sati)"
        description = "Saturn is transiting the 2nd house from natal Moon. Stabilizing finances and familial responsibilities as the cycle completes."
        severity = "moderate"
    elif house_from_moon == 4:
        phase_name = "Dhaiya (Ardhashtama Shani / 4th House)"
        description = "Saturn transiting 4th from Moon (2.5-year sub-period), demanding patience with domestic tranquility and career foundations."
        severity = "moderate"
    elif house_from_moon == 8:
        phase_name = "Dhaiya (Ashtama Shani / 8th House)"
        description = "Saturn transiting 8th from Moon. Calls for careful health habits, avoiding reckless speculation, and internal maturity."
        severity = "high"

    return {
        "is_in_sade_sati": is_sade_sati,
        "is_in_dhaiya": house_from_moon in (4, 8),
        "house_from_natal_moon": house_from_moon,
        "phase": phase_name,
        "severity": severity,
        "description": description,
        "remedies": [
            "Lighting a mustard oil lamp under a Peepal tree on Saturdays",
            "Chanting Shani Beej Mantra: Om Sham Shanaicharaya Namah",
            "Recitation of Hanuman Chalisa",
            "Donation of black sesame seeds and iron vessels to the needy"
        ]
    }

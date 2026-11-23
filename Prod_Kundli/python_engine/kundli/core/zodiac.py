"""Zodiac definitions, Rashis, lords, elements, natures, and polarities."""
from typing import Dict, Any, List

ZODIAC_SIGNS: List[str] = [
    "Aries", "Taurus", "Gemini", "Cancer",
    "Leo", "Virgo", "Libra", "Scorpio",
    "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

SANSKRIT_SIGNS: List[str] = [
    "Mesha", "Vrishabha", "Mithuna", "Karka",
    "Simha", "Kanya", "Tula", "Vrischika",
    "Dhanu", "Makara", "Kumbha", "Meena"
]

SIGN_LORDS: Dict[str, str] = {
    "Aries": "Mars",
    "Taurus": "Venus",
    "Gemini": "Mercury",
    "Cancer": "Moon",
    "Leo": "Sun",
    "Virgo": "Mercury",
    "Libra": "Venus",
    "Scorpio": "Mars",
    "Sagittarius": "Jupiter",
    "Capricorn": "Saturn",
    "Aquarius": "Saturn",
    "Pisces": "Jupiter"
}

SIGN_ELEMENTS: Dict[str, str] = {
    "Aries": "Fire", "Taurus": "Earth", "Gemini": "Air", "Cancer": "Water",
    "Leo": "Fire", "Virgo": "Earth", "Libra": "Air", "Scorpio": "Water",
    "Sagittarius": "Fire", "Capricorn": "Earth", "Aquarius": "Air", "Pisces": "Water"
}

SIGN_MOBILITY: Dict[str, str] = {
    "Aries": "Chara (Movable)", "Taurus": "Sthira (Fixed)", "Gemini": "Dwiswabhava (Dual)",
    "Cancer": "Chara (Movable)", "Leo": "Sthira (Fixed)", "Virgo": "Dwiswabhava (Dual)",
    "Libra": "Chara (Movable)", "Scorpio": "Sthira (Fixed)", "Sagittarius": "Dwiswabhava (Dual)",
    "Capricorn": "Chara (Movable)", "Aquarius": "Sthira (Fixed)", "Pisces": "Dwiswabhava (Dual)"
}

SIGN_VARNA: Dict[str, str] = {
    "Aries": "Kshatriya", "Leo": "Kshatriya", "Sagittarius": "Kshatriya",
    "Taurus": "Vaishya", "Virgo": "Vaishya", "Capricorn": "Vaishya",
    "Gemini": "Shudra", "Libra": "Shudra", "Aquarius": "Shudra",
    "Cancer": "Brahmin", "Scorpio": "Brahmin", "Pisces": "Brahmin"
}

SIGN_VASHYA: Dict[str, str] = {
    "Aries": "Chatushpada", "Taurus": "Chatushpada",
    "Gemini": "Manava", "Cancer": "Jalachara",
    "Leo": "Vanchara", "Virgo": "Manava",
    "Libra": "Manava", "Scorpio": "Keeta",
    "Sagittarius": "Manava",  # First half Manava, second Chatushpada
    "Capricorn": "Jalachara", # First half Chatushpada, second Jalachara
    "Aquarius": "Manava", "Pisces": "Jalachara"
}


def get_sign_from_longitude(longitude: float) -> Dict[str, Any]:
    """Given a 0-360 longitude, return the sign name, sign number (1-12), and degree within sign."""
    lon = longitude % 360.0
    sign_index = int(lon // 30)
    sign_name = ZODIAC_SIGNS[sign_index]
    degree_in_sign = lon - (sign_index * 30.0)
    return {
        "sign_index": sign_index,
        "sign_number": sign_index + 1,
        "sign": sign_name,
        "sanskrit_name": SANSKRIT_SIGNS[sign_index],
        "sign_lord": SIGN_LORDS[sign_name],
        "degree_in_sign": degree_in_sign,
        "element": SIGN_ELEMENTS[sign_name],
        "mobility": SIGN_MOBILITY[sign_name]
    }

"""Nakshatras, Padas, lords, deities, and attributes."""
from typing import Dict, Any, List

NAKSHATRAS: List[str] = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Moola", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
    "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

NAKSHATRA_LORDS: List[str] = [
    "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury",
    "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury",
    "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"
]

# Gana: Deva, Manushya, Rakshasa
NAKSHATRA_GANA: List[str] = [
    "Deva", "Manushya", "Rakshasa", "Manushya", "Deva", "Manushya",
    "Deva", "Deva", "Rakshasa", "Rakshasa", "Manushya", "Manushya",
    "Deva", "Rakshasa", "Deva", "Rakshasa", "Deva", "Rakshasa",
    "Rakshasa", "Manushya", "Manushya", "Deva", "Rakshasa", "Rakshasa",
    "Manushya", "Manushya", "Deva"
]

# Nadi: Aadi (Vata), Madhya (Pitta), Antya (Kapha)
NAKSHATRA_NADI: List[str] = [
    "Aadi", "Madhya", "Antya", "Antya", "Madhya", "Aadi",
    "Aadi", "Madhya", "Antya", "Antya", "Madhya", "Aadi",
    "Aadi", "Madhya", "Antya", "Antya", "Madhya", "Aadi",
    "Aadi", "Madhya", "Antya", "Antya", "Madhya", "Aadi",
    "Aadi", "Madhya", "Antya"
]

# Yoni animals (14 pairs = 28, mapped to 27 nakshatras)
NAKSHATRA_YONI: List[str] = [
    "Horse", "Elephant", "Sheep", "Serpent", "Serpent", "Dog",
    "Cat", "Sheep", "Cat", "Rat", "Rat", "Cow",
    "Buffalo", "Tiger", "Buffalo", "Tiger", "Deer", "Deer",
    "Dog", "Monkey", "Mongoose", "Monkey", "Lion", "Horse",
    "Lion", "Cow", "Elephant"
]

# Rajju classification: Pada (Feet), Kati (Waist), Nabhi (Navel), Kantha (Neck), Shira (Head)
NAKSHATRA_RAJJU: List[str] = [
    "Pada", "Kati", "Nabhi", "Kantha", "Shira", "Kantha",
    "Nabhi", "Kati", "Pada", "Pada", "Kati", "Nabhi",
    "Kantha", "Shira", "Kantha", "Nabhi", "Kati", "Pada",
    "Pada", "Kati", "Nabhi", "Kantha", "Shira", "Kantha",
    "Nabhi", "Kati", "Pada"
]


def get_nakshatra_from_longitude(longitude: float) -> Dict[str, Any]:
    """Given 0-360 sidereal longitude, calculate Nakshatra, Pada, Lord, Gana, Nadi, Yoni, Rajju."""
    lon = longitude % 360.0
    nak_span = 360.0 / 27.0  # 13.333333333333334 degrees = 13°20'
    pada_span = nak_span / 4.0  # 3.3333333333333335 degrees = 3°20'

    nak_index = int(lon // nak_span)
    nak_name = NAKSHATRAS[nak_index]
    lon_in_nak = lon - (nak_index * nak_span)
    pada = int(lon_in_nak // pada_span) + 1

    return {
        "nakshatra_index": nak_index,
        "nakshatra_number": nak_index + 1,
        "nakshatra": nak_name,
        "nakshatra_lord": NAKSHATRA_LORDS[nak_index],
        "nakshatra_pada": pada,
        "degree_in_nakshatra": lon_in_nak,
        "nakshatra_span": nak_span,
        "pada_span": pada_span,
        "gana": NAKSHATRA_GANA[nak_index],
        "nadi": NAKSHATRA_NADI[nak_index],
        "yoni": NAKSHATRA_YONI[nak_index],
        "rajju": NAKSHATRA_RAJJU[nak_index]
    }

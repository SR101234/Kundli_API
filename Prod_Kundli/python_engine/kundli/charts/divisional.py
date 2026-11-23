"""Divisional Charts (Vargas) calculation engine: D1 to D60."""
from typing import Dict, Any, List
from kundli.core.zodiac import ZODIAC_SIGNS, SIGN_LORDS

# Standard 16 Shodashavargas:
# D1: Rashi (30° per division)
# D2: Hora (15° per division: Sun in Leo, Moon in Cancer based on odd/even sign)
# D3: Drekkana (10° per division: 1st 10° same sign, 2nd 10° 5th from it, 3rd 10° 9th from it)
# D4: Chaturthamsha (7°30': 1st, 4th, 7th, 10th from sign)
# D7: Saptamsha (4°17'8.57": odd signs from same sign, even signs from 7th)
# D9: Navamsha (3°20': Aries for fire signs, Capricorn for earth, Libra for air, Cancer for water)
# D10: Dashamsha (3°: odd signs from same, even signs from 9th)
# D12: Dwadashamsha (2°30': starts from same sign)
# D16: Shodashamsha (1°52'30": Aries for movable, Leo for fixed, Sagittarius for dual)
# D20: Vimshamsha (1°30': Aries for movable, Sagittarius for fixed, Leo for dual)
# D24: Chaturvimshamsha / Siddhamsa (1°15': Leo for odd signs, Cancer for even signs)
# D27: Saptavimshamsha / Bhamsa (1°06'40": Aries for fire, Cancer for water, Libra for air, Capricorn for earth)
# D30: Trimshamsha (Unequal divisions by Mars, Saturn, Jupiter, Mercury, Venus)
# D40: Khavedamsha (45': Aries for odd, Libra for even)
# D45: Akshavedamsha (40': Aries for movable, Leo for fixed, Sagittarius for dual)
# D60: Shashtiamsha (30': starts from same sign)


def calculate_d1_sign(lon: float) -> int:
    return int((lon % 360.0) // 30.0)


def calculate_d2_sign(lon: float) -> int:
    """Hora (D2): 0-15° and 15-30°.
    In Odd signs: 1st half = Sun (Leo=4), 2nd half = Moon (Cancer=3).
    In Even signs: 1st half = Moon (Cancer=3), 2nd half = Sun (Leo=4).
    """
    sign_idx = int((lon % 360.0) // 30.0)
    deg = lon % 30.0
    is_odd = (sign_idx % 2 == 0)  # 0-indexed: 0=Aries (odd sign)
    if is_odd:
        return 4 if deg < 15.0 else 3  # Leo if < 15, Cancer if >= 15
    else:
        return 3 if deg < 15.0 else 4  # Cancer if < 15, Leo if >= 15


def calculate_d3_sign(lon: float) -> int:
    """Drekkana (D3): 10° per division.
    1st 10°: Same sign (offset 0)
    2nd 10°: 5th sign from it (offset 4)
    3rd 10°: 9th sign from it (offset 8)
    """
    sign_idx = int((lon % 360.0) // 30.0)
    deg = lon % 30.0
    part = int(deg // 10.0)
    offsets = [0, 4, 8]
    return (sign_idx + offsets[min(part, 2)]) % 12


def calculate_d4_sign(lon: float) -> int:
    """Chaturthamsha (D4): 7°30' each.
    1st: 1st (same sign)
    2nd: 4th from sign (+3)
    3rd: 7th from sign (+6)
    4th: 10th from sign (+9)
    """
    sign_idx = int((lon % 360.0) // 30.0)
    deg = lon % 30.0
    part = int(deg // 7.5)
    return (sign_idx + min(part, 3) * 3) % 12


def calculate_d7_sign(lon: float) -> int:
    """Saptamsha (D7): 30/7 = 4.2857° each.
    In Odd signs: count starts from same sign.
    In Even signs: count starts from 7th sign from it (+6).
    """
    sign_idx = int((lon % 360.0) // 30.0)
    deg = lon % 30.0
    part = int(deg // (30.0 / 7.0))
    is_odd = (sign_idx % 2 == 0)
    start_sign = sign_idx if is_odd else (sign_idx + 6) % 12
    return (start_sign + min(part, 6)) % 12


def calculate_d9_sign(lon: float) -> int:
    """Navamsha (D9): 3°20' (3.3333°) each.
    Fiery signs (Aries 0, Leo 4, Sag 8): start from Aries (0).
    Earthy signs (Taurus 1, Virgo 5, Cap 9): start from Capricorn (9).
    Airy signs (Gemini 2, Libra 6, Aqua 10): start from Libra (6).
    Watery signs (Cancer 3, Scorpio 7, Pisces 11): start from Cancer (3).
    """
    sign_idx = int((lon % 360.0) // 30.0)
    deg = lon % 30.0
    part = int(deg // (30.0 / 9.0))
    
    triplicity = sign_idx % 4
    start_map = {0: 0, 1: 9, 2: 6, 3: 3}  # Fire: Aries, Earth: Cap, Air: Libra, Water: Cancer
    start_sign = start_map[triplicity]
    return (start_sign + min(part, 8)) % 12


def calculate_d10_sign(lon: float) -> int:
    """Dashamsha (D10): 3° each.
    Odd signs: starts from same sign.
    Even signs: starts from 9th sign from it (+8).
    """
    sign_idx = int((lon % 360.0) // 30.0)
    deg = lon % 30.0
    part = int(deg // 3.0)
    is_odd = (sign_idx % 2 == 0)
    start_sign = sign_idx if is_odd else (sign_idx + 8) % 12
    return (start_sign + min(part, 9)) % 12


def calculate_d12_sign(lon: float) -> int:
    """Dwadashamsha (D12): 2°30' (2.5°) each.
    Starts from the sign itself.
    """
    sign_idx = int((lon % 360.0) // 30.0)
    deg = lon % 30.0
    part = int(deg // 2.5)
    return (sign_idx + min(part, 11)) % 12


def calculate_d16_sign(lon: float) -> int:
    """Shodashamsha (D16): 1°52'30" (1.875°) each.
    Movable signs (0, 3, 6, 9): starts from Aries (0).
    Fixed signs (1, 4, 7, 10): starts from Leo (4).
    Dual signs (2, 5, 8, 11): starts from Sagittarius (8).
    """
    sign_idx = int((lon % 360.0) // 30.0)
    deg = lon % 30.0
    part = int(deg // 1.875)
    mobility = sign_idx % 3  # 0=Movable, 1=Fixed, 2=Dual
    start_map = {0: 0, 1: 4, 2: 8}
    return (start_map[mobility] + min(part, 15)) % 12


def calculate_d20_sign(lon: float) -> int:
    """Vimshamsha (D20): 1°30' (1.5°) each.
    Movable: Aries (0), Fixed: Sagittarius (8), Dual: Leo (4).
    """
    sign_idx = int((lon % 360.0) // 30.0)
    deg = lon % 30.0
    part = int(deg // 1.5)
    mobility = sign_idx % 3
    start_map = {0: 0, 1: 8, 2: 4}
    return (start_map[mobility] + min(part, 19)) % 12


def calculate_d24_sign(lon: float) -> int:
    """Chaturvimshamsha (D24): 1°15' (1.25°) each.
    Odd signs: starts from Leo (4).
    Even signs: starts from Cancer (3).
    """
    sign_idx = int((lon % 360.0) // 30.0)
    deg = lon % 30.0
    part = int(deg // 1.25)
    is_odd = (sign_idx % 2 == 0)
    start_sign = 4 if is_odd else 3
    return (start_sign + min(part, 23)) % 12


def calculate_d27_sign(lon: float) -> int:
    """Saptavimshamsha / Bhamsa (D27): 1°06'40" (1.1111°) each.
    Fiery: Aries (0), Earthy: Cancer (3), Airy: Libra (6), Watery: Capricorn (9).
    """
    sign_idx = int((lon % 360.0) // 30.0)
    deg = lon % 30.0
    part = int(deg // (30.0 / 27.0))
    triplicity = sign_idx % 4
    start_map = {0: 0, 1: 3, 2: 6, 3: 9}
    return (start_map[triplicity] + min(part, 26)) % 12


def calculate_d30_sign(lon: float) -> int:
    """Trimshamsha (D30): Unequal divisions.
    Odd signs:
      0-5°: Mars (Aries=0)
      5-10°: Saturn (Aquarius=10)
      10-18°: Jupiter (Sagittarius=8)
      18-25°: Mercury (Gemini=2)
      25-30°: Venus (Libra=6)
    Even signs:
      0-5°: Venus (Taurus=1)
      5-12°: Mercury (Virgo=5)
      12-20°: Jupiter (Pisces=11)
      20-25°: Saturn (Capricorn=9)
      25-30°: Mars (Scorpio=7)
    """
    sign_idx = int((lon % 360.0) // 30.0)
    deg = lon % 30.0
    is_odd = (sign_idx % 2 == 0)
    if is_odd:
        if deg < 5.0: return 0
        elif deg < 10.0: return 10
        elif deg < 18.0: return 8
        elif deg < 25.0: return 2
        else: return 6
    else:
        if deg < 5.0: return 1
        elif deg < 12.0: return 5
        elif deg < 20.0: return 11
        elif deg < 25.0: return 9
        else: return 7


def calculate_d40_sign(lon: float) -> int:
    """Khavedamsha (D40): 45' (0.75°) each.
    Odd signs: starts from Aries (0).
    Even signs: starts from Libra (6).
    """
    sign_idx = int((lon % 360.0) // 30.0)
    deg = lon % 30.0
    part = int(deg // 0.75)
    is_odd = (sign_idx % 2 == 0)
    start_sign = 0 if is_odd else 6
    return (start_sign + min(part, 39)) % 12


def calculate_d45_sign(lon: float) -> int:
    """Akshavedamsha (D45): 40' (0.6667°) each.
    Movable: Aries (0), Fixed: Leo (4), Dual: Sagittarius (8).
    """
    sign_idx = int((lon % 360.0) // 30.0)
    deg = lon % 30.0
    part = int(deg // (30.0 / 45.0))
    mobility = sign_idx % 3
    start_map = {0: 0, 1: 4, 2: 8}
    return (start_map[mobility] + min(part, 44)) % 12


def calculate_d60_sign(lon: float) -> int:
    """Shashtiamsha (D60): 30' (0.5°) each.
    Starts from the sign itself.
    """
    sign_idx = int((lon % 360.0) // 30.0)
    deg = lon % 30.0
    part = int(deg // 0.5)
    return (sign_idx + min(part, 59)) % 12


DIVISION_CALCULATORS = {
    "D1": (calculate_d1_sign, "Rashi", "Overall life"),
    "D2": (calculate_d2_sign, "Hora", "Wealth and prosperity"),
    "D3": (calculate_d3_sign, "Drekkana", "Siblings, courage, vitality"),
    "D4": (calculate_d4_sign, "Chaturthamsha", "Property, fixed assets, fortune"),
    "D7": (calculate_d7_sign, "Saptamsha", "Children and progeny"),
    "D9": (calculate_d9_sign, "Navamsha", "Dharma, marriage, inner potential"),
    "D10": (calculate_d10_sign, "Dashamsha", "Career, profession, social standing"),
    "D12": (calculate_d12_sign, "Dwadashamsha", "Parents and lineage"),
    "D16": (calculate_d16_sign, "Shodashamsha", "Vehicles, comforts, happiness"),
    "D20": (calculate_d20_sign, "Vimshamsha", "Spirituality and religious inclination"),
    "D24": (calculate_d24_sign, "Chaturvimshamsha", "Education, learning, intelligence"),
    "D27": (calculate_d27_sign, "Bhamsa", "Strengths, stamina, physical endurance"),
    "D30": (calculate_d30_sign, "Trimshamsha", "Misfortunes, evils, difficulties"),
    "D40": (calculate_d40_sign, "Khavedamsha", "Subtle auspicious/inauspicious effects"),
    "D45": (calculate_d45_sign, "Akshavedamsha", "General character and all matters"),
    "D60": (calculate_d60_sign, "Shashtiamsha", "Past life karma and root destiny")
}


def generate_divisional_chart(
    division_code: str,
    ascendant_longitude: float,
    planet_longitudes: Dict[str, float]
) -> Dict[str, Any]:
    """Calculate the planetary placements and houses for any divisional chart (D1 to D60)."""
    div_info = DIVISION_CALCULATORS.get(division_code, DIVISION_CALCULATORS["D9"])
    calc_func = div_info[0]
    
    asc_sign_idx = calc_func(ascendant_longitude)
    asc_sign_name = ZODIAC_SIGNS[asc_sign_idx]

    placements = {}
    house_planets = {i: [] for i in range(1, 13)}

    for p_name, lon in planet_longitudes.items():
        p_sign_idx = calc_func(lon)
        p_sign_name = ZODIAC_SIGNS[p_sign_idx]
        house = ((p_sign_idx - asc_sign_idx) % 12) + 1
        placements[p_name] = {
            "planet": p_name,
            "sign": p_sign_name,
            "sign_index": p_sign_idx,
            "sign_lord": SIGN_LORDS[p_sign_name],
            "house": house
        }
        house_planets[house].append(p_name)

    return {
        "division": division_code,
        "name": div_info[1],
        "traditional_use": div_info[2],
        "ascendant_sign": asc_sign_name,
        "ascendant_sign_index": asc_sign_idx,
        "placements": placements,
        "house_planets": house_planets
    }

"""Ashtakoota 36-Gun Milan system for marriage compatibility."""
from typing import Dict, Any, List, Tuple
from pydantic import BaseModel
from kundli.core.zodiac import ZODIAC_SIGNS, SIGN_LORDS
from kundli.core.nakshatra import get_nakshatra_from_longitude

# Varna hierarchy order: Brahmin (4) > Kshatriya (3) > Vaishya (2) > Shudra (1)
VARNA_RANKS = {"Brahmin": 4, "Kshatriya": 3, "Vaishya": 2, "Shudra": 1}
SIGN_VARNA = {
    "Cancer": "Brahmin", "Scorpio": "Brahmin", "Pisces": "Brahmin",
    "Aries": "Kshatriya", "Leo": "Kshatriya", "Sagittarius": "Kshatriya",
    "Taurus": "Vaishya", "Virgo": "Vaishya", "Capricorn": "Vaishya",
    "Gemini": "Shudra", "Libra": "Shudra", "Aquarius": "Shudra"
}

# Vashya classification
SIGN_VASHYA = {
    "Aries": "Chatushpada", "Taurus": "Chatushpada",
    "Gemini": "Manava", "Cancer": "Jalachara",
    "Leo": "Vanchara", "Virgo": "Manava",
    "Libra": "Manava", "Scorpio": "Keeta",
    "Sagittarius": "Manava", "Capricorn": "Jalachara",
    "Aquarius": "Manava", "Pisces": "Jalachara"
}

# Sworn natural enemy Yonis (0 points)
ENEMY_YONIS = {
    ("Cow", "Tiger"), ("Tiger", "Cow"),
    ("Elephant", "Lion"), ("Lion", "Elephant"),
    ("Horse", "Buffalo"), ("Buffalo", "Horse"),
    ("Dog", "Deer"), ("Deer", "Dog"),
    ("Serpent", "Mongoose"), ("Mongoose", "Serpent"),
    ("Monkey", "Sheep"), ("Sheep", "Monkey"),
    ("Cat", "Rat"), ("Rat", "Cat")
}


class KootaScore(BaseModel):
    name: str
    max_score: float
    obtained_score: float
    description: str
    groom_attribute: str
    bride_attribute: str
    has_dosha: bool = False
    cancellation: str = ""


def calculate_varna(groom_sign: str, bride_sign: str) -> KootaScore:
    g_v = SIGN_VARNA[groom_sign]
    b_v = SIGN_VARNA[bride_sign]
    score = 1.0 if VARNA_RANKS[g_v] >= VARNA_RANKS[b_v] else 0.0
    return KootaScore(
        name="Varna (Ego & Work Capacity)",
        max_score=1.0,
        obtained_score=score,
        description="Spiritual and mental compatibility; ego refinement.",
        groom_attribute=g_v,
        bride_attribute=b_v
    )


def calculate_vashya(groom_sign: str, bride_sign: str) -> KootaScore:
    g_v = SIGN_VASHYA[groom_sign]
    b_v = SIGN_VASHYA[bride_sign]
    if g_v == b_v:
        score = 2.0
    elif (g_v == "Manava" and b_v == "Chatushpada") or (g_v == "Vanchara" and b_v == "Jalachara"):
        score = 1.0
    else:
        score = 0.5
    return KootaScore(
        name="Vashya (Dominance & Mutual Attraction)",
        max_score=2.0,
        obtained_score=score,
        description="Mutual magnetic attraction and natural harmony in power dynamic.",
        groom_attribute=g_v,
        bride_attribute=b_v
    )


def calculate_tara(g_nak_idx: int, b_nak_idx: int) -> KootaScore:
    """Tara / Dina: Nakshatra counting distance modulo 9."""
    # From bride to groom
    b_to_g = ((g_nak_idx - b_nak_idx) % 27) + 1
    rem_bg = b_to_g % 9
    ausp_bg = rem_bg in (2, 4, 6, 8, 9, 0)

    # From groom to bride
    g_to_b = ((b_nak_idx - g_nak_idx) % 27) + 1
    rem_gb = g_to_b % 9
    ausp_gb = rem_gb in (2, 4, 6, 8, 9, 0)

    if ausp_bg and ausp_gb:
        score = 3.0
    elif ausp_bg or ausp_gb:
        score = 1.5
    else:
        score = 0.0

    return KootaScore(
        name="Tara (Destiny & Well-being)",
        max_score=3.0,
        obtained_score=score,
        description="Health, longevity, and mutual prosperity.",
        groom_attribute=f"Tara rem: {rem_gb}",
        bride_attribute=f"Tara rem: {rem_bg}"
    )


def calculate_yoni(g_yoni: str, b_yoni: str) -> KootaScore:
    if g_yoni == b_yoni:
        score = 4.0
    elif (g_yoni, b_yoni) in ENEMY_YONIS:
        score = 0.0
    else:
        score = 2.0  # Friendly/neutral
    return KootaScore(
        name="Yoni (Physical & Biological Compatibility)",
        max_score=4.0,
        obtained_score=score,
        description="Biological compatibility, intimacy, and instinctual harmony.",
        groom_attribute=g_yoni,
        bride_attribute=b_yoni,
        has_dosha=(score == 0.0)
    )


def calculate_graha_maitri(g_sign: str, b_sign: str) -> KootaScore:
    g_lord = SIGN_LORDS[g_sign]
    b_lord = SIGN_LORDS[b_sign]
    if g_lord == b_lord:
        score = 5.0
    else:
        # Standard friendships
        friends_map = {
            "Sun": ["Moon", "Mars", "Jupiter"],
            "Moon": ["Sun", "Mercury"],
            "Mars": ["Sun", "Moon", "Jupiter"],
            "Mercury": ["Sun", "Venus"],
            "Jupiter": ["Sun", "Moon", "Mars"],
            "Venus": ["Mercury", "Saturn"],
            "Saturn": ["Mercury", "Venus"]
        }
        g_likes_b = b_lord in friends_map.get(g_lord, [])
        b_likes_g = g_lord in friends_map.get(b_lord, [])
        if g_likes_b and b_likes_g:
            score = 5.0
        elif g_likes_b or b_likes_g:
            score = 3.0
        else:
            score = 1.0

    return KootaScore(
        name="Graha Maitri (Psychological & Emotional Affinity)",
        max_score=5.0,
        obtained_score=score,
        description="Intellectual friendship and worldview alignment.",
        groom_attribute=f"{g_sign} ({g_lord})",
        bride_attribute=f"{b_sign} ({b_lord})"
    )


def calculate_gana(g_gana: str, b_gana: str) -> KootaScore:
    if g_gana == b_gana:
        score = 6.0
    elif (g_gana == "Deva" and b_gana == "Manushya") or (g_gana == "Manushya" and b_gana == "Deva"):
        score = 5.0
    elif (g_gana == "Deva" and b_gana == "Rakshasa"):
        score = 1.0
    else:
        score = 0.0  # Manushya + Rakshasa
    return KootaScore(
        name="Gana (Temperament & Behavioral Alignment)",
        max_score=6.0,
        obtained_score=score,
        description="Spiritual nature and domestic harmony.",
        groom_attribute=g_gana,
        bride_attribute=b_gana,
        has_dosha=(score == 0.0)
    )


def calculate_bhakoot(g_sign_idx: int, b_sign_idx: int, g_sign: str, b_sign: str) -> KootaScore:
    """Bhakoot: 7 points based on sign distance.
    Inauspicious: 2/12, 6/8, 9/5.
    """
    diff = ((g_sign_idx - b_sign_idx) % 12) + 1
    has_dosha = diff in (2, 6, 8, 9, 12)
    score = 0.0 if has_dosha else 7.0
    canc = ""

    # Cancellation: Same lord (e.g. Aries-Scorpio, Taurus-Libra) or mutual friends
    g_lord = SIGN_LORDS[g_sign]
    b_lord = SIGN_LORDS[b_sign]
    if has_dosha and (g_lord == b_lord):
        score = 7.0
        canc = f"Bhakoot Dosha cancelled because both signs are owned by {g_lord}."
        has_dosha = False

    return KootaScore(
        name="Bhakoot (Family Welfare & Prosperity)",
        max_score=7.0,
        obtained_score=score,
        description="Financial prosperity and growth of the family lineage.",
        groom_attribute=g_sign,
        bride_attribute=b_sign,
        has_dosha=has_dosha,
        cancellation=canc
    )


def calculate_nadi(g_nadi: str, b_nadi: str, g_nak: str, b_nak: str, g_sign: str, b_sign: str) -> KootaScore:
    """Nadi: 8 points. Same nadi = 0 (Nadi Dosha)."""
    has_dosha = (g_nadi == b_nadi)
    score = 0.0 if has_dosha else 8.0
    canc = ""

    # Classical Nadi Dosha cancellation:
    # 1. Different nakshatras in the same sign
    # 2. Same nakshatra but different signs
    if has_dosha:
        if g_sign == b_sign and g_nak != b_nak:
            score = 8.0
            canc = "Nadi Dosha cancelled: Different nakshatras in the same rashi."
            has_dosha = False
        elif g_sign != b_sign and g_nak == b_nak:
            score = 8.0
            canc = "Nadi Dosha cancelled: Same nakshatra falling in different rashis."
            has_dosha = False

    return KootaScore(
        name="Nadi (Genetics, Health & Progeny)",
        max_score=8.0,
        obtained_score=score,
        description="Genetic compatibility, physiological vitality, and progeny health.",
        groom_attribute=g_nadi,
        bride_attribute=b_nadi,
        has_dosha=has_dosha,
        cancellation=canc
    )


def calculate_ashtakoota_milan(
    groom_moon_lon: float,
    bride_moon_lon: float
) -> Dict[str, Any]:
    """Calculate full 36-Gun Ashtakoota compatibility."""
    g_nak = get_nakshatra_from_longitude(groom_moon_lon)
    b_nak = get_nakshatra_from_longitude(bride_moon_lon)

    g_sign_idx = int(groom_moon_lon // 30)
    b_sign_idx = int(bride_moon_lon // 30)
    g_sign = ZODIAC_SIGNS[g_sign_idx]
    b_sign = ZODIAC_SIGNS[b_sign_idx]

    kootas: List[KootaScore] = [
        calculate_varna(g_sign, b_sign),
        calculate_vashya(g_sign, b_sign),
        calculate_tara(g_nak["nakshatra_index"], b_nak["nakshatra_index"]),
        calculate_yoni(g_nak["yoni"], b_nak["yoni"]),
        calculate_graha_maitri(g_sign, b_sign),
        calculate_gana(g_nak["gana"], b_nak["gana"]),
        calculate_bhakoot(g_sign_idx, b_sign_idx, g_sign, b_sign),
        calculate_nadi(g_nak["nadi"], b_nak["nadi"], g_nak["nakshatra"], b_nak["nakshatra"], g_sign, b_sign)
    ]

    total_obtained = sum(k.obtained_score for k in kootas)
    
    if total_obtained >= 28:
        verdict = "Excellent Match (Uttam Milan)"
    elif total_obtained >= 18:
        verdict = "Good & Compatible Match (Madhyam Milan)"
    else:
        verdict = "Low Compatibility Score (Varjya / Not Recommended)"

    doshas_detected = [k.name for k in kootas if k.has_dosha]

    return {
        "total_score": round(total_obtained, 1),
        "maximum_score": 36.0,
        "percentage": round((total_obtained / 36.0) * 100, 1),
        "verdict": verdict,
        "doshas_detected": doshas_detected,
        "koota_breakdown": [k.model_dump() for k in kootas]
    }

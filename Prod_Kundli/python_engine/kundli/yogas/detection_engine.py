"""Vedic Yogas detection engine returning structured rule evaluations."""
from typing import Dict, Any, List
from pydantic import BaseModel
from kundli.core.zodiac import ZODIAC_SIGNS, SIGN_LORDS
from kundli.core.house_lords import KENDRAS, TRIKONAS, DUSTHANAS


class YogaEvaluation(BaseModel):
    name: str
    detected: bool
    category: str
    description: str
    conditions_met: List[str]
    conditions_failed: List[str]
    severity: str = "auspicious"
    rule_version: str = "1.0"


def evaluate_yogas(
    planets: Dict[str, Any],
    ascendant_sign_idx: int,
    house_planets: Dict[int, List[str]],
    house_lords: Dict[int, Dict[str, Any]]
) -> List[YogaEvaluation]:
    """Evaluate classical Vedic auspicious yogas with structured condition evidence."""
    results: List[YogaEvaluation] = []

    # 1. Gajakesari Yoga: Jupiter in a Kendra (1, 4, 7, 10) from Moon
    jup = planets.get("Jupiter")
    moon = planets.get("Moon")
    if jup and moon:
        # Distance from Moon's house to Jupiter's house
        h_diff = ((jup.house - moon.house) % 12) + 1
        is_kendra = h_diff in [1, 4, 7, 10]
        c_met, c_fail = [], []
        if is_kendra:
            c_met.append(f"Jupiter is in {h_diff}th house (Kendra) from Moon")
        else:
            c_fail.append(f"Jupiter is in {h_diff}th house from Moon (not 1, 4, 7, 10)")

        results.append(YogaEvaluation(
            name="Gajakesari Yoga",
            detected=is_kendra,
            category="Raj Yoga",
            description="Grants wisdom, eminence, lasting prosperity, and commanding respect in society.",
            conditions_met=c_met,
            conditions_failed=c_fail,
            severity="highly_auspicious"
        ))

    # 2. Budhaditya Yoga: Sun and Mercury together in the same house
    sun = planets.get("Sun")
    merc = planets.get("Mercury")
    if sun and merc:
        same_house = (sun.house == merc.house)
        c_met, c_fail = [], []
        if same_house:
            c_met.append(f"Sun and Mercury are conjunct in House {sun.house} ({sun.sign})")
            if merc.is_combust:
                c_met.append("Mercury is combust; yoga manifests mildly through sharp intellectual analytical ability.")
            else:
                c_met.append("Mercury is free from deep combustion; sharp intellect and executive capability.")
        else:
            c_fail.append(f"Sun is in House {sun.house} while Mercury is in House {merc.house}")

        results.append(YogaEvaluation(
            name="Budhaditya Yoga",
            detected=same_house,
            category="Dhana / Intellectual Yoga",
            description="Combination of Sun (atman/authority) and Mercury (buddhi/intellect) giving learning and high administrative competence.",
            conditions_met=c_met,
            conditions_failed=c_fail,
            severity="auspicious"
        ))

    # 3. Panch Mahapurusha Yogas (Mars, Mercury, Jupiter, Venus, Saturn in Own/Exalted in Kendra)
    mahapurusha_configs = [
        ("Mars", "Ruchaka Yoga", "courage, leadership, military/executive authority", ["Aries", "Scorpio"], "Capricorn"),
        ("Mercury", "Bhadra Yoga", "intellectual brilliance, oratory, commerce", ["Gemini", "Virgo"], "Virgo"),
        ("Jupiter", "Hamsa Yoga", "virtue, spiritual wisdom, righteous governance", ["Sagittarius", "Pisces"], "Cancer"),
        ("Venus", "Malavya Yoga", "luxuries, arts, magnetism, conjugal joy", ["Taurus", "Libra"], "Pisces"),
        ("Saturn", "Sasa Yoga", "discipline, enduring political power, mass leadership", ["Capricorn", "Aquarius"], "Libra"),
    ]

    for p_name, yoga_name, meaning, own_signs, exalt_sign in mahapurusha_configs:
        p = planets.get(p_name)
        if not p:
            continue
        in_kendra = p.house in KENDRAS
        in_dignity = (p.sign in own_signs) or (p.sign == exalt_sign)
        c_met, c_fail = [], []

        if in_kendra:
            c_met.append(f"{p_name} is in Kendra (House {p.house})")
        else:
            c_fail.append(f"{p_name} is in House {p.house} (not a Kendra)")

        if in_dignity:
            c_met.append(f"{p_name} is in its own/exalted sign ({p.sign})")
        else:
            c_fail.append(f"{p_name} is in {p.sign} (not own or exalted)")

        detected = in_kendra and in_dignity
        results.append(YogaEvaluation(
            name=yoga_name,
            detected=detected,
            category="Panch Mahapurusha",
            description=f"One of the 5 Great Human Yogas formed by {p_name}, endowing the native with {meaning}.",
            conditions_met=c_met,
            conditions_failed=c_fail,
            severity="highly_auspicious" if detected else "neutral"
        ))

    # 4. Vipreet Raj Yoga (6th, 8th, 12th lords in 6, 8, 12)
    # Harsha Yoga (6th lord in 6, 8, or 12)
    # Sarala Yoga (8th lord in 6, 8, or 12)
    # Vimala Yoga (12th lord in 6, 8, or 12)
    vipreet_configs = [
        (6, "Harsha Yoga", "Immunity from adversaries, victory over challenges, robust vitality"),
        (8, "Sarala Yoga", "Sudden prosperity, fearlessness, resilience against unexpected obstacles"),
        (12, "Vimala Yoga", "Independent prosperity, spiritual realization, noble expenditure")
    ]
    for h_num, v_name, v_desc in vipreet_configs:
        h_lord_name = house_lords[h_num]["lord"]
        lord_p = planets.get(h_lord_name)
        if lord_p:
            placed_h = lord_p.house
            is_vry = placed_h in DUSTHANAS
            c_met, c_fail = [], []
            if is_vry:
                c_met.append(f"Lord of house {h_num} ({h_lord_name}) is placed in dusthana house {placed_h}")
            else:
                c_fail.append(f"Lord of house {h_num} ({h_lord_name}) is in auspicious house {placed_h}")
            results.append(YogaEvaluation(
                name=f"Vipreet Raj Yoga ({v_name})",
                detected=is_vry,
                category="Vipreet Raj Yoga",
                description=v_desc,
                conditions_met=c_met,
                conditions_failed=c_fail,
                severity="auspicious" if is_vry else "neutral"
            ))

    # 5. Kendra-Trikona Raj Yoga (Conjunction of a Kendra lord and a Trikona lord)
    kendra_lords = {house_lords[h]["lord"] for h in KENDRAS}
    trikona_lords = {house_lords[h]["lord"] for h in TRIKONAS}
    found_raj_yogas = []
    for k_lord in kendra_lords:
        for t_lord in trikona_lords:
            if k_lord != t_lord and k_lord in planets and t_lord in planets:
                kp = planets[k_lord]
                tp = planets[t_lord]
                if kp.house == tp.house:
                    found_raj_yogas.append(f"{k_lord} (Kendra lord) conjunct {t_lord} (Trikona lord) in House {kp.house}")

    results.append(YogaEvaluation(
        name="Kendra-Trikona Raj Yoga",
        detected=len(found_raj_yogas) > 0,
        category="Raj Yoga",
        description="Union of Vishnu sthanas (Kendras) and Lakshmi sthanas (Trikonas), bestowing sovereign power, elevation, and fortune.",
        conditions_met=found_raj_yogas if found_raj_yogas else [],
        conditions_failed=["No direct conjunction between Kendra and Trikona lords"] if not found_raj_yogas else [],
        severity="highly_auspicious" if found_raj_yogas else "neutral"
    ))

    # 6. Neech Bhanga Raj Yoga (Cancellation of debilitation)
    for p_name, p in planets.items():
        if getattr(p, "is_debilitated", False) or (p_name in ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn") and p.degree_in_sign and p.sign == {"Sun": "Libra", "Moon": "Scorpio", "Mars": "Cancer", "Mercury": "Pisces", "Jupiter": "Capricorn", "Venus": "Virgo", "Saturn": "Aries"}.get(p_name)):
            # Debilitated planet found! Check cancellation
            # Rule 1: The lord of the debilitated sign is in Kendra from Lagna or Moon
            deb_sign_lord = SIGN_LORDS[p.sign]
            lord_p = planets.get(deb_sign_lord)
            c_met, c_fail = [], []
            cancelled = False
            if lord_p:
                if lord_p.house in KENDRAS:
                    cancelled = True
                    c_met.append(f"Lord of debilitation sign {p.sign} ({deb_sign_lord}) is in Kendra (House {lord_p.house}) from Lagna")
                if moon:
                    diff_m = ((lord_p.house - moon.house) % 12) + 1
                    if diff_m in KENDRAS:
                        cancelled = True
                        c_met.append(f"Lord of debilitation sign {p.sign} ({deb_sign_lord}) is in Kendra ({diff_m}th) from Moon")

            results.append(YogaEvaluation(
                name=f"Neech Bhanga Raj Yoga ({p_name})",
                detected=cancelled,
                category="Raj Yoga",
                description=f"Debilitation of {p_name} is cancelled and transformed into high accomplishment through perseverance.",
                conditions_met=c_met,
                conditions_failed=["Debilitation cancellation criteria not satisfied"] if not cancelled else [],
                severity="auspicious" if cancelled else "neutral"
            ))

    # 7. Chandra-Mangal Yoga (Moon conjunct Mars)
    mars = planets.get("Mars")
    if moon and mars:
        cm_detected = (moon.house == mars.house)
        results.append(YogaEvaluation(
            name="Chandra-Mangal Yoga",
            detected=cm_detected,
            category="Dhana Yoga",
            description="Union of Moon and Mars creating formidable financial enterprise, resource accumulation, and commercial drive.",
            conditions_met=[f"Moon and Mars are conjunct in House {moon.house}"] if cm_detected else [],
            conditions_failed=[f"Moon is in House {moon.house} and Mars is in House {mars.house}"] if not cm_detected else [],
            severity="auspicious" if cm_detected else "neutral"
        ))

    return results

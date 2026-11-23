"""Vedic Doshas detection engine with detailed conditions, severity, and cancellations."""
from typing import Dict, Any, List
from pydantic import BaseModel
from kundli.core.zodiac import ZODIAC_SIGNS, SIGN_LORDS


class DoshaEvaluation(BaseModel):
    name: str
    detected: bool
    severity: str  # high, medium, mild, cancelled, none
    description: str
    is_cancelled: bool = False
    cancellation_reasons: List[str] = []
    conditions_met: List[str] = []
    conditions_failed: List[str] = []
    remedies: List[str] = []
    rule_version: str = "1.0"


def evaluate_doshas(
    planets: Dict[str, Any],
    ascendant_sign_idx: int,
    house_planets: Dict[int, List[str]],
    house_lords: Dict[int, Dict[str, Any]]
) -> List[DoshaEvaluation]:
    """Evaluate classical Vedic doshas: Manglik, Kaal Sarp, Pitra, Guru Chandal, Kemadruma, Gand Mool, Grahan, Shrapit."""
    results: List[DoshaEvaluation] = []

    # 1. Manglik / Kuja Dosha (Mars in 1, 4, 7, 8, 12 from Lagna, or from Moon/Venus)
    mars = planets.get("Mars")
    moon = planets.get("Moon")
    venus = planets.get("Venus")
    if mars:
        m_house = mars.house
        # Standard North/South traditions include houses 1, 4, 7, 8, 12 (South adds 2nd)
        manglik_houses = [1, 2, 4, 7, 8, 12]
        is_manglik_lagna = m_house in manglik_houses
        
        c_met, c_fail = [], []
        cancellations = []

        if is_manglik_lagna:
            c_met.append(f"Mars is situated in House {m_house} from Lagna")
            
            # Classical Mangal Dosha Cancellation Rules:
            # 1. Mars in Aries in 1st house
            if m_house == 1 and mars.sign == "Aries":
                cancellations.append("Mars in own sign Aries in 1st house cancels dosha.")
            # 2. Mars in Scorpio in 4th house
            if m_house == 4 and mars.sign == "Scorpio":
                cancellations.append("Mars in own sign Scorpio in 4th house cancels dosha.")
            # 3. Mars in Capricorn (exalted) in 1st, 4th, 7th, 8th or 12th
            if mars.sign == "Capricorn":
                cancellations.append("Mars is exalted in Capricorn, mitigating maleficence.")
            # 4. Mars in Leo or Sagittarius in 8th house
            if m_house == 8 and mars.sign in ("Leo", "Sagittarius"):
                cancellations.append(f"Mars in {mars.sign} in 8th house cancels dosha.")
            # 5. Mars in Taurus or Libra (Venus signs) in 12th house
            if m_house == 12 and mars.sign in ("Taurus", "Libra"):
                cancellations.append(f"Mars in {mars.sign} in 12th house cancels dosha.")
            # 6. Conjunction with Jupiter or aspected by Jupiter
            jup = planets.get("Jupiter")
            if jup and (jup.house == m_house or ((jup.house - m_house) % 12 in (4, 6, 8))):
                cancellations.append("Jupiter is conjunct or casting protective drishti on Mars.")
        else:
            c_fail.append(f"Mars is in House {m_house} (not 1, 2, 4, 7, 8, 12)")

        is_cancelled = len(cancellations) > 0
        severity = "none" if not is_manglik_lagna else ("cancelled" if is_cancelled else ("high" if m_house in (1, 7, 8) else "medium"))

        results.append(DoshaEvaluation(
            name="Manglik / Kuja Dosha",
            detected=is_manglik_lagna,
            severity=severity,
            description="Influence of Mars on marital harmony and temperament. Requires balanced matching.",
            is_cancelled=is_cancelled,
            cancellation_reasons=cancellations,
            conditions_met=c_met,
            conditions_failed=c_fail,
            remedies=["Hanuman Chalisa recitation", "Kumbh Vivah if severe", "Charitable donation of red lentils"]
        ))

    # 2. Kaal Sarp Dosha (All 7 planets hemmed between Rahu and Ketu)
    rahu = planets.get("Rahu")
    ketu = planets.get("Ketu")
    if rahu and ketu:
        r_lon = rahu.longitude
        k_lon = ketu.longitude
        
        # Check arc 1 (Rahu to Ketu) and arc 2 (Ketu to Rahu)
        traditional_7 = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
        in_arc_1 = 0
        in_arc_2 = 0

        for p_name in traditional_7:
            p_lon = planets[p_name].longitude
            # In arc from Rahu to Ketu counter-clockwise
            diff_r_to_p = (p_lon - r_lon) % 360.0
            diff_r_to_k = (k_lon - r_lon) % 360.0  # Approx 180 degrees
            
            if diff_r_to_p < diff_r_to_k:
                in_arc_1 += 1
            else:
                in_arc_2 += 1

        is_purna_ks = (in_arc_1 == 7 or in_arc_2 == 7)
        is_anshik_ks = (in_arc_1 == 6 or in_arc_2 == 6)
        ks_detected = is_purna_ks or is_anshik_ks

        # 12 types based on Rahu's house
        kaal_sarp_types = {
            1: "Anant Kaal Sarp Dosha",
            2: "Kulik Kaal Sarp Dosha",
            3: "Vasuki Kaal Sarp Dosha",
            4: "Shankhpal Kaal Sarp Dosha",
            5: "Padma Kaal Sarp Dosha",
            6: "Mahapadma Kaal Sarp Dosha",
            7: "Takshak Kaal Sarp Dosha",
            8: "Karkotak Kaal Sarp Dosha",
            9: "Shankhachood Kaal Sarp Dosha",
            10: "Ghatak Kaal Sarp Dosha",
            11: "Vishdhar Kaal Sarp Dosha",
            12: "Sheshnag Kaal Sarp Dosha"
        }
        specific_type = kaal_sarp_types.get(rahu.house, "Kaal Sarp Dosha")
        c_met, c_fail = [], []
        if is_purna_ks:
            c_met.append(f"All 7 planets are hemmed on one side of Rahu-Ketu axis (Purna Kaal Sarp: {specific_type})")
        elif is_anshik_ks:
            c_met.append(f"6 of 7 planets are hemmed on one side of Rahu-Ketu axis (Anshik / Partial Kaal Sarp: {specific_type})")
        else:
            c_fail.append("Planets are distributed on both sides of the Rahu-Ketu nodal axis.")

        results.append(DoshaEvaluation(
            name=f"Kaal Sarp Dosha ({specific_type})" if ks_detected else "Kaal Sarp Dosha",
            detected=ks_detected,
            severity="high" if is_purna_ks else ("medium" if is_anshik_ks else "none"),
            description="Planetary confinement by nodal axis creating early struggle followed by dramatic rise later in life.",
            is_cancelled=False,
            conditions_met=c_met,
            conditions_failed=c_fail,
            remedies=["Maha Mrityunjaya Japa", "Rahu-Ketu shanti", "Worship of Lord Shiva on Mondays"]
        ))

    # 3. Pitra Dosha (Affliction to Sun or 9th house/lord)
    sun = planets.get("Sun")
    h9_lord = house_lords[9]["lord"]
    pitra_detected = False
    c_met, c_fail = [], []
    if sun and rahu and sun.house == rahu.house:
        pitra_detected = True
        c_met.append(f"Sun is conjunct Rahu in House {sun.house} (Paternal lineage affliction)")
    if sun and planets.get("Saturn") and sun.house == planets["Saturn"].house:
        pitra_detected = True
        c_met.append(f"Sun is conjunct Saturn in House {sun.house}")
    if house_lords[9]["lord"] in planets and planets[house_lords[9]["lord"]].house in (6, 8, 12):
        pitra_detected = True
        c_met.append(f"9th house lord ({h9_lord}) is placed in dusthana (House {planets[h9_lord].house})")

    if not pitra_detected:
        c_fail.append("No adverse conjunction with Sun or affliction to 9th house lord found.")

    results.append(DoshaEvaluation(
        name="Pitra Dosha",
        detected=pitra_detected,
        severity="medium" if pitra_detected else "none",
        description="Karmic debt relating to ancestors, calling for charity, respect for elders, and tarpan.",
        conditions_met=c_met,
        conditions_failed=c_fail,
        remedies=["Tarpan during Pitru Paksha", "Feeding cows and crows", "Surya Arghya with water"]
    ))

    # 4. Guru Chandal Dosha (Jupiter conjunct Rahu or Ketu)
    jup = planets.get("Jupiter")
    if jup and rahu and ketu:
        gc_rahu = (jup.house == rahu.house)
        gc_ketu = (jup.house == ketu.house)
        gc_detected = gc_rahu or gc_ketu
        c_met, c_fail = [], []
        if gc_rahu:
            c_met.append(f"Jupiter is conjunct Rahu in House {jup.house}")
        if gc_ketu:
            c_met.append(f"Jupiter is conjunct Ketu in House {jup.house}")
        if not gc_detected:
            c_fail.append("Jupiter is not conjunct Rahu or Ketu.")

        results.append(DoshaEvaluation(
            name="Guru Chandal Dosha",
            detected=gc_detected,
            severity="medium" if gc_detected else "none",
            description="Affliction to spiritual and intellectual discernment, bringing unorthodox beliefs.",
            conditions_met=c_met,
            conditions_failed=c_fail,
            remedies=["Brihaspati Beej Mantra", "Respecting spiritual teachers and preceptors", "Wearing yellow sapphire if suitable"]
        ))

    # 5. Kemadruma Yoga (No planets in 2nd and 12th from Moon, excluding Sun/Rahu/Ketu)
    if moon:
        m_house = moon.house
        h_prev = 12 if m_house == 1 else m_house - 1
        h_next = 1 if m_house == 12 else m_house + 1
        
        valid_planets_prev = [p for p in house_planets.get(h_prev, []) if p not in ("Sun", "Rahu", "Ketu")]
        valid_planets_next = [p for p in house_planets.get(h_next, []) if p not in ("Sun", "Rahu", "Ketu")]

        has_kemadruma = (len(valid_planets_prev) == 0 and len(valid_planets_next) == 0)
        c_met, c_fail = [], []
        cancellations = []

        if has_kemadruma:
            c_met.append(f"No planets (excluding Sun/Rahu/Ketu) in 2nd ({h_next}) or 12th ({h_prev}) from Moon")
            # Cancellation: Any planet in Kendra from Lagna or Moon
            kendra_planets_from_lagna = sum(len(house_planets.get(h, [])) for h in KENDRAS)
            if kendra_planets_from_lagna > 0:
                cancellations.append("Planets present in Kendras from Lagna, cancelling Kemadruma effects.")
        else:
            c_fail.append("Planets exist in 2nd or 12th house from Moon.")

        results.append(DoshaEvaluation(
            name="Kemadruma Yoga",
            detected=has_kemadruma,
            severity="cancelled" if (has_kemadruma and cancellations) else ("medium" if has_kemadruma else "none"),
            description="Isolation of the Moon indicating psychological solitary periods, neutralized by Kendra planets.",
            is_cancelled=len(cancellations) > 0,
            cancellation_reasons=cancellations,
            conditions_met=c_met,
            conditions_failed=c_fail,
            remedies=["Worship of Lord Shiva and Goddess Parvati", "Wearing silver"]
        ))

    # 6. Gand Mool Dosha (Birth in Mercury or Ketu nakshatras)
    if moon:
        m_nak = moon.nakshatra
        gand_mool_naks = ["Ashwini", "Ashlesha", "Magha", "Jyeshtha", "Moola", "Revati"]
        is_gm = m_nak in gand_mool_naks
        results.append(DoshaEvaluation(
            name="Gand Mool Dosha",
            detected=is_gm,
            severity="mild" if is_gm else "none",
            description=f"Moon is placed in Gand Mool nakshatra ({m_nak}), requiring Mool Shanti ceremony in infancy.",
            conditions_met=[f"Moon is in {m_nak} (Pada {moon.nakshatra_pada})"] if is_gm else [],
            conditions_failed=[f"Moon is in {m_nak} (not a Gand Mool nakshatra)"] if not is_gm else [],
            remedies=["Gand Mool Shanti on the 27th day after birth", "Ganesh Puja"]
        ))

    return results

"""Master Kundli Orchestration Engine unifying all Vedic and KP calculation layers."""
from datetime import datetime
from typing import Dict, Any, List, Optional
from kundli.astronomy.coordinates import BirthInput, to_utc_datetime
from kundli.astronomy.ephemeris import calculate_julian_day
from kundli.astronomy.planets import calculate_planet_positions
from kundli.astronomy.houses import calculate_houses_and_ascendant, assign_houses_to_planets
from kundli.core.house_lords import get_house_lords, get_planets_in_houses
from kundli.core.dignity import get_planet_dignity
from kundli.core.aspects import calculate_mutual_aspects, calculate_aspected_houses
from kundli.core.panchang import calculate_panchang
from kundli.charts.d1 import build_rashi_chart, build_chandra_kundli, build_surya_kundli
from kundli.charts.divisional import generate_divisional_chart, DIVISION_CALCULATORS
from kundli.charts.chart_renderer import render_north_indian_svg, render_south_indian_svg
from kundli.kp.cusps import calculate_kp_cusp_table, calculate_kp_planet_table
from kundli.kp.significators import calculate_kp_significators
from kundli.kp.ruling_planets import calculate_ruling_planets
from kundli.ashtakavarga.bav import calculate_bav
from kundli.ashtakavarga.sav import calculate_sav
from kundli.ashtakavarga.reductions import trikona_shodhana, ekadhipatya_shodhana, calculate_shodhya_pinda
from kundli.dasha.vimshottari import VimshottariDasha
from kundli.dasha.yogini import calculate_yogini_dasha
from kundli.yogas.detection_engine import evaluate_yogas
from kundli.doshas.detection_engine import evaluate_doshas
from kundli.transits.gochar import calculate_transits
from kundli.transits.sade_sati import evaluate_sade_sati
from kundli.strengths.shadbala import calculate_shadbala


def generate_complete_kundli(birth: BirthInput) -> Dict[str, Any]:
    """Execute complete end-to-end Kundli calculation pipeline."""
    # 1. Coordinate and Time conversions
    utc_dt = to_utc_datetime(birth.date, birth.time, birth.timezone)
    tjd_ut = calculate_julian_day(utc_dt)
    local_dt = datetime.combine(birth.date, birth.time)

    # 2. Planetary positions & Houses
    planets = calculate_planet_positions(tjd_ut, birth.ayanamsa, birth.node_type)
    houses_result = calculate_houses_and_ascendant(
        tjd_ut, birth.latitude, birth.longitude, birth.ayanamsa, birth.house_system
    )
    ascendant = houses_result.ascendant
    asc_sign_idx = ascendant.sign_index

    # Assign houses (Whole Sign and Bhava Chalit) to planets
    assign_houses_to_planets(planets, asc_sign_idx, houses_result.houses)

    # 3. House Lords and Occupancy
    house_lords = get_house_lords(asc_sign_idx)
    house_occupants = get_planets_in_houses(planets)
    house_planets_by_house = {h: [p_name for p_name, p in planets.items() if p.house == h] for h in range(1, 13)}

    # 4. Planetary Dignities
    planet_house_map = {p_name: p.house for p_name, p in planets.items()}
    dignity_report = {}
    for p_name, p in planets.items():
        if p_name in ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"):
            dig = get_planet_dignity(p_name, p.sign, p.degree_in_sign, p.house, planet_house_map)
            dignity_report[p_name] = dig

    # 5. Panchang at birth
    panchang = calculate_panchang(
        tjd_ut,
        planets["Sun"].longitude,
        planets["Moon"].longitude,
        local_dt,
        birth.latitude,
        birth.longitude
    )

    # 6. Charts (D1, Chandra, Surya, D9 Navamsha, D10 Dashamsha)
    planet_lons = {p_name: p.longitude for p_name, p in planets.items()}
    d1_chart = build_rashi_chart(ascendant, planets)
    chandra_chart = build_chandra_kundli(planets)
    surya_chart = build_surya_kundli(planets)

    divisional_charts = {}
    for div_key in ["D2", "D3", "D4", "D7", "D9", "D10", "D12", "D16", "D20", "D24", "D27", "D30", "D40", "D45", "D60"]:
        divisional_charts[div_key] = generate_divisional_chart(div_key, ascendant.longitude, planet_lons)

    # SVG Renderers for D1
    north_svg = render_north_indian_svg(d1_chart["house_signs"], d1_chart["house_planets"])
    south_svg = render_south_indian_svg(d1_chart["house_signs"], d1_chart["house_planets"])

    # 7. KP Astrology (Sub-lords, Cusps, 4-step Significators, Ruling Planets)
    kp_cusp_table = calculate_kp_cusp_table(houses_result.houses)
    kp_planet_table = calculate_kp_planet_table(planets)
    kp_significators = calculate_kp_significators(kp_planet_table, kp_cusp_table)
    ruling_planets = calculate_ruling_planets(
        panchang.vara_lord,
        planets["Moon"].longitude,
        ascendant.longitude,
        planets["Rahu"].longitude,
        planets["Ketu"].longitude
    )

    # 8. Ashtakavarga Engine
    planet_signs = {p_name: p.sign_index for p_name, p in planets.items()}
    bav_tables = calculate_bav(planet_signs, asc_sign_idx)
    sav_result = calculate_sav(bav_tables)

    # Ashtakavarga reductions for Moon & Mars
    moon_shodhana = trikona_shodhana(bav_tables["Moon"])
    moon_ekadhipatya = ekadhipatya_shodhana(moon_shodhana, planet_signs)
    moon_shodhya_pinda = calculate_shodhya_pinda(moon_ekadhipatya, planet_signs)

    # 9. Dasha Engine (Vimshottari & Yogini)
    vim_dasha = VimshottariDasha().calculate_dasha_timeline(local_dt, planets["Moon"].longitude)
    yogini_dasha = calculate_yogini_dasha(local_dt, planets["Moon"].longitude)

    # 10. Yogas & Doshas Engine
    yogas = evaluate_yogas(planets, asc_sign_idx, house_planets_by_house, house_lords)
    doshas = evaluate_doshas(planets, asc_sign_idx, house_planets_by_house, house_lords)

    # 11. Current Transits (Gochar) & Sade Sati
    transits = calculate_transits(planets["Moon"].sign_index, asc_sign_idx)
    # Find current Saturn transit sign
    current_saturn = next((t for t in transits["transits"] if t["planet"] == "Saturn"), None)
    saturn_transit_idx = (planets["Moon"].sign_index + current_saturn["house_from_moon"] - 1) % 12 if current_saturn else planets["Moon"].sign_index
    sade_sati = evaluate_sade_sati(planets["Moon"].sign_index, saturn_transit_idx)

    # 12. Strengths (Shadbala)
    shadbala = calculate_shadbala(planets, ascendant.longitude)

    # 13. Aspects
    mutual_aspects = calculate_mutual_aspects(planets)

    return {
        "metadata": {
            "name": birth.name,
            "birth_date": str(birth.date),
            "birth_time": str(birth.time),
            "timezone": birth.timezone,
            "latitude": birth.latitude,
            "longitude": birth.longitude,
            "ayanamsa": birth.ayanamsa,
            "ayanamsa_value": houses_result.ayanamsa_value,
            "house_system": birth.house_system,
            "julian_day": round(tjd_ut, 6),
            "utc_datetime": utc_dt.isoformat()
        },
        "ascendant": ascendant.model_dump(),
        "midheaven": houses_result.midheaven.model_dump(),
        "panchang": panchang.model_dump(),
        "planets": {k: v.model_dump() for k, v in planets.items()},
        "dignities": dignity_report,
        "houses": [h.model_dump() for h in houses_result.houses],
        "house_lords": house_lords,
        "house_occupants": house_occupants,
        "charts": {
            "d1_rashi": d1_chart,
            "chandra_kundli": chandra_chart,
            "surya_kundli": surya_chart,
            "divisional": divisional_charts,
            "svg_north_indian": north_svg,
            "svg_south_indian": south_svg
        },
        "kp_astrology": {
            "cusps": [c.model_dump() for c in kp_cusp_table],
            "planets": [p.model_dump() for p in kp_planet_table],
            "significators": {
                "planet_significators": [ps.model_dump() for ps in kp_significators["planet_significators"]],
                "house_significators": [hs.model_dump() for hs in kp_significators["house_significators"]]
            },
            "ruling_planets": ruling_planets
        },
        "ashtakavarga": {
            "bav": bav_tables,
            "sav": sav_result,
            "sample_shodhya_pinda_moon": moon_shodhya_pinda
        },
        "dasha": {
            "vimshottari": vim_dasha,
            "yogini": yogini_dasha
        },
        "yogas": [y.model_dump() for y in yogas],
        "doshas": [d.model_dump() for d in doshas],
        "transits": transits,
        "sade_sati": sade_sati,
        "shadbala": shadbala,
        "aspects": mutual_aspects
    }

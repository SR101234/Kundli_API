"""Sarvashtakavarga (SAV) matrix, sign totals, and strength evaluation."""
from typing import Dict, Any, List
from kundli.core.zodiac import ZODIAC_SIGNS
from kundli.ashtakavarga.bav import calculate_bav


def calculate_sav(bav_tables: Dict[str, List[int]]) -> Dict[str, Any]:
    """Calculate the 12-sign Sarvashtakavarga total bindus and validation.
    Total bindus across all 12 signs must equal 337 in standard Parashari.
    """
    sav_sign_totals = [0] * 12

    for planet, bindus in bav_tables.items():
        for s_idx in range(12):
            sav_sign_totals[s_idx] += bindus[s_idx]

    grand_total = sum(sav_sign_totals)
    
    # Sign strength analysis:
    # 28 points is the average (337 / 12 = 28.08).
    # > 28 is strong/favorable, < 28 is weak.
    sign_strengths = []
    for idx, total in enumerate(sav_sign_totals):
        sign_strengths.append({
            "sign_index": idx,
            "sign": ZODIAC_SIGNS[idx],
            "total_bindus": total,
            "status": "Strong" if total >= 28 else "Weak",
            "difference_from_average": round(total - 28.08, 2)
        })

    return {
        "bav": bav_tables,
        "sav_totals": sav_sign_totals,
        "grand_total": grand_total,
        "is_traditional_337": (grand_total == 337),
        "sign_analysis": sign_strengths
    }

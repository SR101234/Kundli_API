"""Combined Marriage Compatibility analysis including Ashtakoota and Manglik matching."""
from typing import Dict, Any, List
from kundli.matching.ashtakoota import calculate_ashtakoota_milan


def evaluate_marriage_compatibility(
    groom_chart: Dict[str, Any],
    bride_chart: Dict[str, Any]
) -> Dict[str, Any]:
    """Perform complete marriage matching between Groom and Bride charts."""
    groom_moon_lon = groom_chart["planets"]["Moon"]["longitude"]
    bride_moon_lon = bride_chart["planets"]["Moon"]["longitude"]

    ashtakoota = calculate_ashtakoota_milan(groom_moon_lon, bride_moon_lon)

    # Manglik comparison
    g_manglik = next((d for d in groom_chart.get("doshas", []) if "Manglik" in d["name"]), None)
    b_manglik = next((d for d in bride_chart.get("doshas", []) if "Manglik" in d["name"]), None)

    g_is_m = g_manglik and g_manglik["detected"] and not g_manglik["is_cancelled"]
    b_is_m = b_manglik and b_manglik["detected"] and not b_manglik["is_cancelled"]

    if g_is_m and b_is_m:
        manglik_verdict = "Both are Manglik: Dosha is mutually cancelled and harmonized."
        manglik_compatible = True
    elif not g_is_m and not b_is_m:
        manglik_verdict = "Neither is Manglik: Complete harmony from Mars influence."
        manglik_compatible = True
    else:
        manglik_verdict = "One partner is Manglik while the other is not. Astrological remedies or detailed chart inspection recommended."
        manglik_compatible = False

    return {
        "ashtakoota": ashtakoota,
        "manglik_matching": {
            "groom_is_manglik": bool(g_is_m),
            "bride_is_manglik": bool(b_is_m),
            "is_compatible": manglik_compatible,
            "verdict": manglik_verdict
        },
        "overall_recommendation": (
            "Recommended for Marriage"
            if (ashtakoota["total_score"] >= 18 and manglik_compatible)
            else "Proceed with Remedial Consultation"
        )
    }

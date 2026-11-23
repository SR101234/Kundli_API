"""FastAPI route handlers for all Kundli API endpoints."""
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from kundli.astronomy.coordinates import BirthInput
from kundli.orchestrator import generate_complete_kundli
from kundli.matching.compatibility import evaluate_marriage_compatibility
from kundli.db.database import get_or_create_user, record_kundli_generation

router = APIRouter(prefix="/api/kundli", tags=["Kundli"])


class CompatibilityRequest(BaseModel):
    groom: BirthInput
    bride: BirthInput


@router.get("/user-quota", summary="Check User Kundli Quota")
def api_get_user_quota(email: str = Query(..., description="User email"), mobile: str = Query("", description="User mobile"), name: str = Query("", description="User name")):
    """Returns the user's current checks used and remaining limit (10)."""
    user = get_or_create_user(name=name, email=email, mobile=mobile)
    return {
        "user_name": user["name"],
        "user_email": user["email"],
        "user_mobile": user["mobile"],
        "checks_used": user["checks_used"],
        "max_limit": user["max_limit"],
        "remaining_checks": user["remaining_checks"],
        "has_quota": user["has_quota"]
    }


@router.post("/generate", summary="Generate Complete Kundli Report")
def api_generate_kundli(birth: BirthInput):
    """Orchestrates all calculation engines, enforces 10 check limit per user, and records logs."""
    user = None
    if birth.user_email:
        user = get_or_create_user(
            name=birth.user_name or birth.name,
            email=birth.user_email,
            mobile=birth.user_mobile or ""
        )
        if user["checks_used"] >= user["max_limit"]:
            raise HTTPException(
                status_code=403,
                detail=f"Check limit reached ({user['checks_used']}/{user['max_limit']} Kundlis used). Contact the administrator to increase your limit."
            )

    try:
        report = generate_complete_kundli(birth)
        
        # Save record & increment check count if user is identified
        if user:
            record_kundli_generation(user, birth, report)
            user_updated = get_or_create_user(user["name"], user["email"], user["mobile"])
            report["user_quota"] = {
                "user_name": user_updated["name"],
                "user_email": user_updated["email"],
                "user_mobile": user_updated["mobile"],
                "checks_used": user_updated["checks_used"],
                "max_limit": user_updated["max_limit"],
                "remaining_checks": user_updated["remaining_checks"]
            }

        return report
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/basic", summary="Generate Basic Kundli (D1, Planets, Panchang)")
def api_basic_kundli(birth: BirthInput):
    """Returns basic birth chart, planetary placements, and birth panchang."""
    try:
        full = generate_complete_kundli(birth)
        return {
            "metadata": full["metadata"],
            "ascendant": full["ascendant"],
            "panchang": full["panchang"],
            "planets": full["planets"],
            "dignities": full["dignities"],
            "d1_rashi": full["charts"]["d1_rashi"],
            "svg_north_indian": full["charts"]["svg_north_indian"],
            "svg_south_indian": full["charts"]["svg_south_indian"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/kp", summary="KP Astrology Calculations")
def api_kp_astrology(birth: BirthInput):
    """Returns KP cuspal positions, planetary sub-lords, significators, and ruling planets."""
    try:
        full = generate_complete_kundli(birth)
        return full["kp_astrology"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ashtakavarga", summary="Ashtakavarga Calculations (BAV, SAV)")
def api_ashtakavarga(birth: BirthInput):
    """Returns Bhinnashtakavarga (BAV), Sarvashtakavarga (SAV 337 points), and Shodhya Pinda."""
    try:
        full = generate_complete_kundli(birth)
        return full["ashtakavarga"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/divisional", summary="Divisional Charts (D1 to D60)")
def api_divisional_charts(birth: BirthInput, division: Optional[str] = Query(None, description="e.g. D9, D10, D60")):
    """Returns all or specific divisional charts."""
    try:
        full = generate_complete_kundli(birth)
        if division:
            div = division.upper()
            if div in full["charts"]["divisional"]:
                return full["charts"]["divisional"][div]
            raise HTTPException(status_code=404, detail=f"Divisional chart {division} not found.")
        return full["charts"]["divisional"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/dasha", summary="Dasha Timelines (Vimshottari & Yogini)")
def api_dasha(birth: BirthInput):
    """Returns full Vimshottari 5-level hierarchy and Yogini dasha."""
    try:
        full = generate_complete_kundli(birth)
        return full["dasha"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/yogas", summary="Yogas Evaluation")
def api_yogas(birth: BirthInput):
    """Detects and returns structured evidence for Vedic Yogas."""
    try:
        full = generate_complete_kundli(birth)
        return {"yogas": full["yogas"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/doshas", summary="Doshas Evaluation & Cancellations")
def api_doshas(birth: BirthInput):
    """Detects Doshas (Manglik, Kaal Sarp, Pitra, etc.) with cancellation checks."""
    try:
        full = generate_complete_kundli(birth)
        return {"doshas": full["doshas"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/matching", summary="Kundli Matching & 36 Gun Milan")
def api_matching(req: CompatibilityRequest):
    """Calculates Ashtakoota 36 Gun Milan and Manglik compatibility for marriage."""
    try:
        groom_chart = generate_complete_kundli(req.groom)
        bride_chart = generate_complete_kundli(req.bride)
        result = evaluate_marriage_compatibility(groom_chart, bride_chart)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/transits", summary="Gochar (Transits) & Sade Sati")
def api_transits(birth: BirthInput):
    """Returns current planetary transits vs natal Moon, and Saturn Sade Sati status."""
    try:
        full = generate_complete_kundli(birth)
        return {
            "transits": full["transits"],
            "sade_sati": full["sade_sati"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/strengths", summary="Planetary Strengths (Shadbala)")
def api_strengths(birth: BirthInput):
    """Returns Shadbala calculations and required Rupas."""
    try:
        full = generate_complete_kundli(birth)
        return full["shadbala"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

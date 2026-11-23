"""Tests for specialized astrology modules: KP, Ashtakavarga, Matching, Dasha."""
from datetime import date, time, datetime
from kundli.astronomy.coordinates import BirthInput
from kundli.orchestrator import generate_complete_kundli
from kundli.matching.ashtakoota import calculate_ashtakoota_milan
from kundli.kp.sublords import get_kp_sub_lord
from kundli.dasha.vimshottari import VimshottariDasha


def test_kp_sublord_calculation():
    # Test Ashwini 0 degrees: Ketu star lord, Ketu sub lord
    res = get_kp_sub_lord(0.1)
    assert res["sign"] == "Aries"
    assert res["sign_lord"] == "Mars"
    assert res["star"] == "Ashwini"
    assert res["star_lord"] == "Ketu"
    assert res["sub_lord"] == "Ketu"

    # Test Ashwini towards the end of Ketu sub-period (e.g. 1 degree)
    # Ketu sub span is 46'40" = 0.7777 deg. So at 1.0 deg it should be Venus!
    res_venus = get_kp_sub_lord(1.0)
    assert res_venus["sub_lord"] == "Venus"


def test_ashtakoota_matching():
    # Moon in Rohini (Taurus, Earth, Vaishya, Chatushpada, Snake, Manushya, Antya)
    # Moon in Revati (Pisces, Water, Brahmin, Jalachara, Elephant, Deva, Antya)
    # Longitude of Rohini ~45 deg, Revati ~355 deg
    milan = calculate_ashtakoota_milan(45.0, 355.0)
    assert milan["total_score"] > 0
    assert milan["maximum_score"] == 36.0
    assert "koota_breakdown" in milan
    assert len(milan["koota_breakdown"]) == 8


def test_vimshottari_dasha_hierarchy():
    dt = datetime(2001, 8, 15, 14, 35, 0)
    # Moon at Cancer 20 deg (Aslesha nakshatra, Lord Mercury)
    dasha_eng = VimshottariDasha()
    res = dasha_eng.calculate_dasha_timeline(dt, moon_longitude=110.0, target_datetime=datetime(2026, 11, 22))
    assert res["first_lord"] == "Mercury"
    assert res["current_running"]["mahadasha"] is not None
    assert len(res["mahadashas"]) == 9

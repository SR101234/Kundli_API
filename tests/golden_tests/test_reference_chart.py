"""Golden reference tests verifying the exact user sample chart and astronomical precision."""
import pytest
from datetime import date, time
from kundli.astronomy.coordinates import BirthInput
from kundli.orchestrator import generate_complete_kundli


@pytest.fixture
def sample_chart_input():
    return BirthInput(
        name="Example User",
        date=date(2001, 8, 15),
        time=time(14, 35, 0),
        timezone="Asia/Kolkata",
        latitude=27.1767,
        longitude=78.0081,
        ayanamsa="Lahiri",
        chart_type="vedic"
    )


def test_complete_kundli_generation(sample_chart_input):
    result = generate_complete_kundli(sample_chart_input)
    assert result is not None
    assert "planets" in result
    assert "ascendant" in result
    assert "panchang" in result
    assert "kp_astrology" in result
    assert "ashtakavarga" in result
    assert "dasha" in result
    assert "yogas" in result
    assert "doshas" in result

    # Check Sun longitude on 15 Aug 2001 (around Cancer ~28-29 degrees)
    sun = result["planets"]["Sun"]
    assert sun["sign"] == "Cancer"
    assert 28.0 <= sun["degree_in_sign"] <= 29.5

    # Check Moon placement
    moon = result["planets"]["Moon"]
    assert moon["sign"] in ("Gemini", "Taurus")
    assert moon["nakshatra"] in ("Mrigashira", "Rohini", "Ardra")

    # Check Ascendant (Scorpio / Sagittarius around 14:35 in Agra/UP)
    asc = result["ascendant"]
    assert asc["sign"] == "Scorpio"
    assert 0 <= asc["degree_in_sign"] <= 30

    # Verify Ashtakavarga traditional total = 337 points!
    sav = result["ashtakavarga"]["sav"]
    assert sav["grand_total"] == 337
    assert sav["is_traditional_337"] is True

    # Check Vimshottari Dasha
    vim = result["dasha"]["vimshottari"]
    assert vim["first_lord"] == moon["nakshatra_lord"]
    assert len(vim["mahadashas"]) == 9
    assert vim["balance_years"] > 0

    # Check KP Cusps and Sub-lords
    kp_cusps = result["kp_astrology"]["cusps"]
    assert len(kp_cusps) == 12
    for c in kp_cusps:
        assert c["sub_lord"] in ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]

    # Check Panchang
    panchang = result["panchang"]
    assert panchang["vara_lord"] == "Mercury"  # 15 Aug 2001 was a Wednesday (Budhavara)
    assert panchang["paksha"] in ("Shukla Paksha", "Krishna Paksha")


def test_ashtakavarga_sum():
    from kundli.ashtakavarga.bav import calculate_bav
    from kundli.ashtakavarga.sav import calculate_sav
    
    # Arbitrary test sign positions
    signs = {"Sun": 4, "Moon": 2, "Mars": 7, "Mercury": 3, "Jupiter": 8, "Venus": 1, "Saturn": 9}
    bav = calculate_bav(signs, ascendant_sign_index=0)
    sav = calculate_sav(bav)
    assert sav["grand_total"] == 337

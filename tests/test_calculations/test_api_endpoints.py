"""API Route tests using FastAPI TestClient."""
from fastapi.testclient import TestClient
from kundli.api.main import app

client = TestClient(app)

SAMPLE_PAYLOAD = {
    "name": "Test User",
    "date": "2001-08-15",
    "time": "14:35:00",
    "timezone": "Asia/Kolkata",
    "latitude": 27.1767,
    "longitude": 78.0081,
    "ayanamsa": "Lahiri",
    "chart_type": "vedic"
}


def test_health_and_root():
    r_health = client.get("/health")
    assert r_health.status_code == 200
    assert r_health.json()["status"] == "healthy"

    r_status = client.get("/api/status")
    assert r_status.status_code == 200
    assert r_status.json()["status"] == "online"

    r_root = client.get("/")
    assert r_root.status_code == 200


def test_api_generate():
    r = client.post("/api/kundli/generate", json=SAMPLE_PAYLOAD)
    assert r.status_code == 200
    data = r.json()
    assert "planets" in data
    assert "kp_astrology" in data
    assert "ashtakavarga" in data
    assert "yogas" in data
    assert "doshas" in data
    assert "charts" in data


def test_api_basic():
    r = client.post("/api/kundli/basic", json=SAMPLE_PAYLOAD)
    assert r.status_code == 200
    data = r.json()
    assert "planets" in data
    assert "ascendant" in data
    assert "panchang" in data
    assert "svg_north_indian" in data


def test_api_kp():
    r = client.post("/api/kundli/kp", json=SAMPLE_PAYLOAD)
    assert r.status_code == 200
    data = r.json()
    assert "cusps" in data
    assert "planets" in data
    assert "significators" in data
    assert "ruling_planets" in data


def test_api_ashtakavarga():
    r = client.post("/api/kundli/ashtakavarga", json=SAMPLE_PAYLOAD)
    assert r.status_code == 200
    data = r.json()
    assert data["sav"]["grand_total"] == 337


def test_api_divisional():
    r = client.post("/api/kundli/divisional", json=SAMPLE_PAYLOAD, params={"division": "D9"})
    assert r.status_code == 200
    data = r.json()
    assert data["division"] == "D9"
    assert data["name"] == "Navamsha"


def test_api_matching():
    r = client.post("/api/kundli/matching", json={
        "groom": SAMPLE_PAYLOAD,
        "bride": {
            **SAMPLE_PAYLOAD,
            "name": "Bride",
            "date": "2002-11-20",
            "time": "10:15:00"
        }
    })
    assert r.status_code == 200
    data = r.json()
    assert "ashtakoota" in data
    assert "total_score" in data["ashtakoota"]
    assert "overall_recommendation" in data

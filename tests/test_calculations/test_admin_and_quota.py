"""Tests for User 10-Check Limit Enforcement, Database Logging, and Admin Panel."""
from fastapi.testclient import TestClient
from kundli.api.main import app
from kundli.db.database import get_or_create_user, adjust_user_limit

client = TestClient(app)
ADMIN_KEY = "admin@kundli2026"


def test_user_creation_and_quota():
    test_email = "testuser_quota@example.com"
    user = get_or_create_user(name="Rahul Sharma", email=test_email, mobile="9876543210")
    assert user["email"] == test_email
    assert user["max_limit"] == 10
    assert user["checks_used"] == 0
    assert user["remaining_checks"] == 10


def test_10_kundli_check_limit_enforcement():
    test_email = "limit_strict_test@example.com"
    # Ensure fresh user with max_limit 10
    user = get_or_create_user(name="Limit User", email=test_email, mobile="9998887770")
    user_id = user["id"]
    adjust_user_limit(user_id, new_limit=10, reset_checks=True)

    # Perform 9 checks
    for i in range(9):
        r = client.post("/api/kundli/generate", json={
            "user_name": "Limit User",
            "user_email": test_email,
            "user_mobile": "9998887770",
            "name": f"Test Child {i+1}",
            "date": "2005-06-10",
            "time": "12:00:00",
            "timezone": "Asia/Kolkata",
            "latitude": 28.6139,
            "longitude": 77.2090
        })
        assert r.status_code == 200

    # 10th check should SUCCEED and exhaust quota
    r_10 = client.post("/api/kundli/generate", json={
        "user_name": "Limit User",
        "user_email": test_email,
        "user_mobile": "9998887770",
        "name": "Test Child 10",
        "date": "2005-06-10",
        "time": "12:00:00",
        "timezone": "Asia/Kolkata",
        "latitude": 28.6139,
        "longitude": 77.2090
    })
    assert r_10.status_code == 200
    data_10 = r_10.json()
    assert data_10["user_quota"]["checks_used"] == 10
    assert data_10["user_quota"]["remaining_checks"] == 0

    # 11th check MUST BE BLOCKED with HTTP 403
    r_11 = client.post("/api/kundli/generate", json={
        "user_name": "Limit User",
        "user_email": test_email,
        "user_mobile": "9998887770",
        "name": "Test Child 11",
        "date": "2005-06-10",
        "time": "12:00:00",
        "timezone": "Asia/Kolkata",
        "latitude": 28.6139,
        "longitude": 77.2090
    })
    assert r_11.status_code == 403
    assert "Check limit reached" in r_11.json()["detail"]


def test_admin_endpoints():
    headers = {"X-Admin-Key": ADMIN_KEY}

    # Stats
    r_stats = client.get("/api/admin/stats", headers=headers)
    assert r_stats.status_code == 200
    stats = r_stats.json()
    assert "total_users" in stats
    assert "total_records" in stats

    # Users list
    r_users = client.get("/api/admin/users", headers=headers)
    assert r_users.status_code == 200
    assert len(r_users.json()["users"]) > 0

    # Kundli generation history with timestamps and birth parameters
    r_records = client.get("/api/admin/records", headers=headers)
    assert r_records.status_code == 200
    records = r_records.json()["records"]
    assert len(records) > 0
    rec = records[0]
    assert "user_name" in rec
    assert "user_email" in rec
    assert "user_mobile" in rec
    assert "seeker_name" in rec
    assert "birth_date" in rec
    assert "birth_time" in rec
    assert "latitude" in rec
    assert "created_at" in rec

    # Admin increases limit for a user
    user_id = records[0]["user_id"]
    r_adjust = client.post(f"/api/admin/users/{user_id}/limit", json={"new_limit": 20, "reset_checks": True}, headers=headers)
    assert r_adjust.status_code == 200
    assert r_adjust.json()["user"]["max_limit"] == 20
    assert r_adjust.json()["user"]["checks_used"] == 0

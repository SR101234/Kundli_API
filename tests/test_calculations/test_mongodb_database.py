"""Dedicated tests for MongoDB database operations, indexing, and aggregations."""
import mongomock
from kundli.db.database import (
    set_test_db,
    get_or_create_user,
    verify_user_quota,
    record_kundli_generation,
    get_admin_stats,
    get_all_users,
    get_all_records,
    adjust_user_limit
)
from kundli.astronomy.coordinates import BirthInput


def test_mongodb_user_lifecycle_and_aggregations():
    # Setup clean test db
    test_db = mongomock.MongoClient()["test_mongo_lifecycle"]
    set_test_db(test_db)

    # 1. Create User
    u1 = get_or_create_user(name="Aarav Patel", email="aarav@example.com", mobile="+919876543211")
    assert u1["name"] == "Aarav Patel"
    assert u1["email"] == "aarav@example.com"
    assert u1["checks_used"] == 0
    assert u1["max_limit"] == 10
    assert u1["remaining_checks"] == 10
    assert u1["has_quota"] is True
    assert "id" in u1

    # 2. Duplicate get_or_create should return existing user and update mobile if new
    u1_again = get_or_create_user(name="Aarav Patel Updated", email="AARAV@example.com", mobile="+919876543212")
    assert u1_again["id"] == u1["id"]
    assert u1_again["mobile"] == "+919876543212"

    # 3. Quota verification
    has_quota, used, limit = verify_user_quota(u1["id"])
    assert has_quota is True
    assert used == 0
    assert limit == 10

    # 4. Record Kundli generation
    birth = BirthInput(
        user_name="Aarav Patel",
        user_email="aarav@example.com",
        user_mobile="+919876543212",
        name="Little Aarav",
        date="2020-01-15",
        time="10:30:00",
        timezone="Asia/Kolkata",
        latitude=19.0760,
        longitude=72.8777
    )
    result = {
        "ascendant": {"sign": "Pisces"},
        "planets": {
            "Moon": {"sign": "Virgo", "nakshatra": "Hasta"}
        }
    }
    rec_id = record_kundli_generation(u1_again, birth, result)
    assert rec_id is not None

    # Verify quota increment
    has_quota2, used2, limit2 = verify_user_quota(u1["id"])
    assert used2 == 1
    assert limit2 == 10

    # 5. Search users
    found = get_all_users(search="aarav")
    assert len(found) >= 1
    assert found[0]["email"] == "aarav@example.com"

    # 6. Search records
    recs = get_all_records(search="Little Aarav")
    assert len(recs) == 1
    assert recs[0]["seeker_name"] == "Little Aarav"
    assert recs[0]["ascendant_sign"] == "Pisces"
    assert recs[0]["moon_sign"] == "Virgo"

    # 7. Adjust user limit
    updated = adjust_user_limit(u1["id"], new_limit=25, reset_checks=True)
    assert updated["max_limit"] == 25
    assert updated["checks_used"] == 0
    assert updated["remaining_checks"] == 25

    # 8. Admin stats
    stats = get_admin_stats()
    assert stats["total_users"] >= 1
    assert stats["total_records"] >= 1

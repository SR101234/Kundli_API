"""MongoDB database manager for User management, 10-check quota enforcement, and Kundli generation audit logs."""
import os
import re
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from bson import ObjectId
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.collection import Collection
from pymongo.database import Database
from kundli.config import MONGO_URI, MONGO_DB_NAME, DEFAULT_CHECK_LIMIT

# Global client and db singleton
_client: Optional[MongoClient] = None
_db: Optional[Database] = None


def get_client() -> MongoClient:
    """Get or create singleton MongoDB client with connection pooling."""
    global _client
    if _client is None:
        # Check if running under mongomock (e.g. for testing)
        if os.environ.get("USE_MONGOMOCK", "").lower() in ("1", "true", "yes"):
            import mongomock
            _client = mongomock.MongoClient()
        else:
            _client = MongoClient(
                MONGO_URI,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=5000,
                maxPoolSize=50,
                minPoolSize=5,
            )
    return _client


def get_db() -> Database:
    """Get or initialize MongoDB database instance with required indexes."""
    global _db
    if _db is None:
        client = get_client()
        _db = client[MONGO_DB_NAME]
        init_db(_db)
    return _db


def set_test_db(custom_db: Database):
    """Override database instance with a mock/test database for unit testing."""
    global _db
    _db = custom_db
    init_db(_db)


def init_db(db: Optional[Database] = None):
    """Ensure indexes on users and kundli_records collections."""
    if db is None:
        db = get_db()
    try:
        # Indexes for users collection
        db.users.create_index([("email", ASCENDING)], unique=True)
        db.users.create_index([("mobile", ASCENDING)])

        # Indexes for kundli_records collection
        db.kundli_records.create_index([("user_id", ASCENDING)])
        db.kundli_records.create_index([("user_email", ASCENDING)])
        db.kundli_records.create_index([("created_at", DESCENDING)])
    except Exception:
        # Index creation may already exist or running on mock without index support
        pass


def _to_object_id_or_val(val: Any) -> Any:
    """Convert string to ObjectId if valid 24-char hex, otherwise return as is."""
    if isinstance(val, ObjectId):
        return val
    s = str(val)
    if ObjectId.is_valid(s):
        return ObjectId(s)
    return s


def _format_user_doc(doc: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """Format MongoDB user document for API and frontend compatibility."""
    if not doc:
        return {}
    res = dict(doc)
    doc_id = str(res.pop("_id", ""))
    res["id"] = doc_id
    checks_used = int(res.get("checks_used", 0))
    max_limit = int(res.get("max_limit", DEFAULT_CHECK_LIMIT))
    res["checks_used"] = checks_used
    res["max_limit"] = max_limit
    res["remaining_checks"] = max(0, max_limit - checks_used)
    res["has_quota"] = res["remaining_checks"] > 0
    return res


def _format_record_doc(doc: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """Format MongoDB kundli record document for API and frontend compatibility."""
    if not doc:
        return {}
    res = dict(doc)
    res["id"] = str(res.pop("_id", ""))
    res["user_id"] = str(res.get("user_id", ""))
    return res


def get_or_create_user(name: str, email: str, mobile: str) -> Dict[str, Any]:
    """Find existing user by email or create new user with 10 Kundli check limit."""
    db = get_db()
    email_clean = email.strip().lower()
    mobile_clean = mobile.strip()
    name_clean = name.strip() or "Seeker"
    now_iso = datetime.now().isoformat()

    existing = db.users.find_one({"email": email_clean})
    if existing:
        update_fields: Dict[str, Any] = {"updated_at": now_iso}
        if name_clean and name_clean != "Seeker":
            update_fields["name"] = name_clean
        if mobile_clean:
            update_fields["mobile"] = mobile_clean

        db.users.update_one({"_id": existing["_id"]}, {"$set": update_fields})
        updated = db.users.find_one({"_id": existing["_id"]})
        return _format_user_doc(updated)

    new_user = {
        "name": name_clean,
        "email": email_clean,
        "mobile": mobile_clean,
        "checks_used": 0,
        "max_limit": DEFAULT_CHECK_LIMIT,
        "created_at": now_iso,
        "updated_at": now_iso
    }
    result = db.users.insert_one(new_user)
    new_user["_id"] = result.inserted_id
    return _format_user_doc(new_user)


def verify_user_quota(user_id: Any) -> Tuple[bool, int, int]:
    """Verify if user has remaining Kundli checks. Returns (has_quota, checks_used, max_limit)."""
    db = get_db()
    oid = _to_object_id_or_val(user_id)
    doc = db.users.find_one({"$or": [{"_id": oid}, {"id": str(user_id)}]})
    if not doc:
        return False, 0, 0
    used = int(doc.get("checks_used", 0))
    limit = int(doc.get("max_limit", DEFAULT_CHECK_LIMIT))
    return (used < limit), used, limit


def record_kundli_generation(user: Dict[str, Any], birth_input: Any, result: Dict[str, Any]) -> str:
    """Atomically increment user's checks_used and record full birth parameters with timestamp."""
    db = get_db()
    user_id_raw = user.get("id") or user.get("_id")
    oid = _to_object_id_or_val(user_id_raw)
    now_dt = datetime.now()
    now_str = now_dt.strftime("%Y-%m-%d %H:%M:%S")
    now_iso = now_dt.isoformat()

    asc_sign = result.get("ascendant", {}).get("sign", "")
    moon_sign = result.get("planets", {}).get("Moon", {}).get("sign", "")
    nakshatra = result.get("planets", {}).get("Moon", {}).get("nakshatra", "")

    # 1. Atomically increment checks_used on user
    db.users.update_one(
        {"$or": [{"_id": oid}, {"id": str(user_id_raw)}]},
        {"$inc": {"checks_used": 1}, "$set": {"updated_at": now_iso}}
    )

    # 2. Record generation log
    record_doc = {
        "user_id": str(user_id_raw),
        "user_name": user.get("name", ""),
        "user_email": user.get("email", ""),
        "user_mobile": user.get("mobile", ""),
        "seeker_name": birth_input.name,
        "birth_date": str(birth_input.date),
        "birth_time": str(birth_input.time),
        "timezone": birth_input.timezone,
        "latitude": float(birth_input.latitude),
        "longitude": float(birth_input.longitude),
        "ayanamsa": birth_input.ayanamsa,
        "house_system": birth_input.house_system,
        "ascendant_sign": asc_sign,
        "moon_sign": moon_sign,
        "nakshatra": nakshatra,
        "created_at": now_str
    }
    rec_result = db.kundli_records.insert_one(record_doc)
    return str(rec_result.inserted_id)


def get_admin_stats() -> Dict[str, Any]:
    """Retrieve aggregate platform metrics for Admin Dashboard."""
    db = get_db()
    total_users = db.users.count_documents({})
    total_records = db.kundli_records.count_documents({})

    # Aggregate sum of checks_used
    pipeline = [{"$group": {"_id": None, "total": {"$sum": "$checks_used"}}}]
    sum_result = list(db.users.aggregate(pipeline))
    total_checks_used = sum_result[0]["total"] if sum_result else 0

    # Users who have reached their max_limit
    limit_reached = db.users.count_documents({"$expr": {"$gte": ["$checks_used", "$max_limit"]}})

    # Records generated today
    today_prefix = datetime.now().strftime("%Y-%m-%d")
    today_records = db.kundli_records.count_documents({"created_at": {"$regex": f"^{today_prefix}"}})

    return {
        "total_users": total_users,
        "total_records": total_records,
        "total_checks_used": total_checks_used,
        "users_limit_reached": limit_reached,
        "records_today": today_records,
        "default_limit": DEFAULT_CHECK_LIMIT
    }


def get_all_users(search: Optional[str] = None, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
    """Get registered users list with search filter and pagination."""
    db = get_db()
    query: Dict[str, Any] = {}
    if search:
        s = search.strip()
        regex_pattern = {"$regex": re.escape(s), "$options": "i"}
        query = {
            "$or": [
                {"name": regex_pattern},
                {"email": regex_pattern},
                {"mobile": regex_pattern}
            ]
        }
    cursor = db.users.find(query).sort("_id", DESCENDING).skip(offset).limit(limit)
    return [_format_user_doc(doc) for doc in cursor]


def get_all_records(search: Optional[str] = None, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
    """Get full Kundli calculation audit records with search and pagination."""
    db = get_db()
    query: Dict[str, Any] = {}
    if search:
        s = search.strip()
        regex_pattern = {"$regex": re.escape(s), "$options": "i"}
        query = {
            "$or": [
                {"user_name": regex_pattern},
                {"user_email": regex_pattern},
                {"user_mobile": regex_pattern},
                {"seeker_name": regex_pattern}
            ]
        }
    cursor = db.kundli_records.find(query).sort("_id", DESCENDING).skip(offset).limit(limit)
    return [_format_record_doc(doc) for doc in cursor]


def adjust_user_limit(user_id: Any, new_limit: Optional[int] = None, reset_checks: bool = False) -> Dict[str, Any]:
    """Admin tool to reset used checks or customize limits for a user."""
    db = get_db()
    oid = _to_object_id_or_val(user_id)
    now_iso = datetime.now().isoformat()

    update_fields: Dict[str, Any] = {"updated_at": now_iso}
    if reset_checks:
        update_fields["checks_used"] = 0
    if new_limit is not None:
        update_fields["max_limit"] = int(new_limit)

    db.users.update_one(
        {"$or": [{"_id": oid}, {"id": str(user_id)}]},
        {"$set": update_fields}
    )
    updated = db.users.find_one({"$or": [{"_id": oid}, {"id": str(user_id)}]})
    if not updated:
        raise ValueError(f"User with ID {user_id} not found")
    return _format_user_doc(updated)

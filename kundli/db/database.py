"""Database manager for User authentication, 10-check quota enforcement, and Kundli history logging."""
import sqlite3
import os
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple

DB_PATH = os.environ.get("KUNDLI_DB_PATH", os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "kundli.db"))


def get_connection():
    """Get a SQLite database connection with row factory enabled."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize database tables with indexes."""
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # 1. Users table (tracks email, mobile, and 10 checks quota)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL COLLATE NOCASE,
                mobile TEXT NOT NULL,
                checks_used INTEGER DEFAULT 0,
                max_limit INTEGER DEFAULT 10,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_mobile ON users(mobile)")

        # 2. Kundli generation records with timestamp and all input parameters
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS kundli_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL REFERENCES users(id),
                user_name TEXT,
                user_email TEXT,
                user_mobile TEXT,
                seeker_name TEXT NOT NULL,
                birth_date TEXT NOT NULL,
                birth_time TEXT NOT NULL,
                timezone TEXT NOT NULL,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                ayanamsa TEXT NOT NULL,
                house_system TEXT NOT NULL,
                ascendant_sign TEXT,
                moon_sign TEXT,
                nakshatra TEXT,
                created_at TEXT NOT NULL
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_records_user_id ON kundli_records(user_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_records_created_at ON kundli_records(created_at)")
        conn.commit()


# Initialize database on module load
init_db()


def get_or_create_user(name: str, email: str, mobile: str) -> Dict[str, Any]:
    """Get existing user by email or create a new user with 10 Kundli check limit."""
    email_clean = email.strip().lower()
    mobile_clean = mobile.strip()
    name_clean = name.strip() or "Seeker"
    now_iso = datetime.now().isoformat()

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email_clean,))
        row = cursor.fetchone()

        if row:
            # Update mobile or name if provided and different
            cursor.execute(
                "UPDATE users SET name = ?, mobile = ?, updated_at = ? WHERE id = ?",
                (name_clean, mobile_clean or row["mobile"], now_iso, row["id"])
            )
            conn.commit()
            cursor.execute("SELECT * FROM users WHERE id = ?", (row["id"],))
            updated_row = cursor.fetchone()
            user_dict = dict(updated_row)
        else:
            cursor.execute(
                """INSERT INTO users (name, email, mobile, checks_used, max_limit, created_at, updated_at)
                   VALUES (?, ?, ?, 0, 10, ?, ?)""",
                (name_clean, email_clean, mobile_clean, now_iso, now_iso)
            )
            conn.commit()
            user_id = cursor.lastrowid
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            user_dict = dict(cursor.fetchone())

    user_dict["remaining_checks"] = max(0, user_dict["max_limit"] - user_dict["checks_used"])
    user_dict["has_quota"] = user_dict["remaining_checks"] > 0
    return user_dict


def verify_user_quota(user_id: int) -> Tuple[bool, int, int]:
    """Verify if user has remaining Kundli checks. Returns (has_quota, checks_used, max_limit)."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT checks_used, max_limit FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        if not row:
            return False, 0, 0
        used = row["checks_used"]
        limit = row["max_limit"]
        return (used < limit), used, limit


def record_kundli_generation(user: Dict[str, Any], birth_input: Any, result: Dict[str, Any]) -> int:
    """Increment checks_used and record the full Kundli birth information with timestamp."""
    user_id = user["id"]
    now_iso = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    asc_sign = result.get("ascendant", {}).get("sign", "")
    moon_sign = result.get("planets", {}).get("Moon", {}).get("sign", "")
    nakshatra = result.get("planets", {}).get("Moon", {}).get("nakshatra", "")

    with get_connection() as conn:
        cursor = conn.cursor()
        
        # 1. Increment checks_used
        cursor.execute(
            "UPDATE users SET checks_used = checks_used + 1, updated_at = ? WHERE id = ?",
            (now_iso, user_id)
        )

        # 2. Insert record
        cursor.execute(
            """INSERT INTO kundli_records (
                user_id, user_name, user_email, user_mobile,
                seeker_name, birth_date, birth_time, timezone,
                latitude, longitude, ayanamsa, house_system,
                ascendant_sign, moon_sign, nakshatra, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                user_id,
                user.get("name", ""),
                user.get("email", ""),
                user.get("mobile", ""),
                birth_input.name,
                str(birth_input.date),
                str(birth_input.time),
                birth_input.timezone,
                birth_input.latitude,
                birth_input.longitude,
                birth_input.ayanamsa,
                birth_input.house_system,
                asc_sign,
                moon_sign,
                nakshatra,
                now_iso
            )
        )
        conn.commit()
        return cursor.lastrowid


def get_admin_stats() -> Dict[str, Any]:
    """Retrieve aggregate statistics for the Admin Dashboard."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM kundli_records")
        total_records = cursor.fetchone()[0]

        cursor.execute("SELECT SUM(checks_used) FROM users")
        total_checks_used = cursor.fetchone()[0] or 0

        # Users who reached their 10 limit
        cursor.execute("SELECT COUNT(*) FROM users WHERE checks_used >= max_limit")
        users_limit_reached = cursor.fetchone()[0]

        # Kundlis generated today
        today_prefix = datetime.now().strftime("%Y-%m-%d")
        cursor.execute("SELECT COUNT(*) FROM kundli_records WHERE created_at LIKE ?", (f"{today_prefix}%",))
        records_today = cursor.fetchone()[0]

    return {
        "total_users": total_users,
        "total_records": total_records,
        "total_checks_used": total_checks_used,
        "users_limit_reached": users_limit_reached,
        "records_today": records_today,
        "default_limit": 10
    }


def get_all_users(search: Optional[str] = None, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
    """Get list of registered users with optional search by name, email, or mobile."""
    with get_connection() as conn:
        cursor = conn.cursor()
        if search:
            q = f"%{search.strip()}%"
            cursor.execute(
                """SELECT * FROM users
                   WHERE name LIKE ? OR email LIKE ? OR mobile LIKE ?
                   ORDER BY id DESC LIMIT ? OFFSET ?""",
                (q, q, q, limit, offset)
            )
        else:
            cursor.execute("SELECT * FROM users ORDER BY id DESC LIMIT ? OFFSET ?", (limit, offset))
        
        rows = cursor.fetchall()
        result = []
        for r in rows:
            d = dict(r)
            d["remaining_checks"] = max(0, d["max_limit"] - d["checks_used"])
            result.append(d)
        return result


def get_all_records(search: Optional[str] = None, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
    """Get history of generated Kundlis with full birth inputs and timestamps."""
    with get_connection() as conn:
        cursor = conn.cursor()
        if search:
            q = f"%{search.strip()}%"
            cursor.execute(
                """SELECT * FROM kundli_records
                   WHERE user_name LIKE ? OR user_email LIKE ? OR user_mobile LIKE ? OR seeker_name LIKE ?
                   ORDER BY id DESC LIMIT ? OFFSET ?""",
                (q, q, q, q, limit, offset)
            )
        else:
            cursor.execute("SELECT * FROM kundli_records ORDER BY id DESC LIMIT ? OFFSET ?", (limit, offset))
        return [dict(r) for r in cursor.fetchall()]


def adjust_user_limit(user_id: int, new_limit: Optional[int] = None, reset_checks: bool = False) -> Dict[str, Any]:
    """Admin function to reset checks or increase limits for a user."""
    now_iso = datetime.now().isoformat()
    with get_connection() as conn:
        cursor = conn.cursor()
        if reset_checks and new_limit is not None:
            cursor.execute("UPDATE users SET checks_used = 0, max_limit = ?, updated_at = ? WHERE id = ?", (new_limit, now_iso, user_id))
        elif reset_checks:
            cursor.execute("UPDATE users SET checks_used = 0, updated_at = ? WHERE id = ?", (now_iso, user_id))
        elif new_limit is not None:
            cursor.execute("UPDATE users SET max_limit = ?, updated_at = ? WHERE id = ?", (new_limit, now_iso, user_id))
        conn.commit()

        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        updated = dict(cursor.fetchone())
        updated["remaining_checks"] = max(0, updated["max_limit"] - updated["checks_used"])
        return updated

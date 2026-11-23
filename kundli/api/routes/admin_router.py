"""Admin API routes for managing users, monitoring Kundli generation logs, and adjusting quotas."""
import os
from fastapi import APIRouter, HTTPException, Query, Header
from pydantic import BaseModel, EmailStr
from typing import Dict, Any, List, Optional
from kundli.db.database import (
    get_admin_stats,
    get_all_users,
    get_all_records,
    adjust_user_limit,
    get_or_create_user
)

router = APIRouter(prefix="/api/admin", tags=["Admin Panel"])
from kundli.config import ADMIN_KEY


class AdminLoginRequest(BaseModel):
    passcode: str


class AdjustLimitRequest(BaseModel):
    new_limit: Optional[int] = None
    reset_checks: bool = False


def verify_admin(x_admin_key: Optional[str] = Header(None)):
    """Simple admin verification header."""
    if not x_admin_key or x_admin_key != ADMIN_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid Admin Key")


@router.post("/login")
def admin_login(req: AdminLoginRequest):
    """Verify admin passcode."""
    if req.passcode == ADMIN_KEY:
        return {"status": "authenticated", "admin_key": ADMIN_KEY}
    raise HTTPException(status_code=401, detail="Invalid admin passcode. Access denied.")


@router.get("/stats")
def api_admin_stats(x_admin_key: Optional[str] = Header(None)):
    """Get aggregate platform metrics."""
    verify_admin(x_admin_key)
    return get_admin_stats()


@router.get("/users")
def api_admin_users(
    search: Optional[str] = Query(None, description="Search by name, email, or mobile"),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    x_admin_key: Optional[str] = Header(None)
):
    """Retrieve registered users list with check limits and contact info."""
    verify_admin(x_admin_key)
    users = get_all_users(search=search, limit=limit, offset=offset)
    return {"users": users, "count": len(users)}


@router.get("/records")
def api_admin_records(
    search: Optional[str] = Query(None, description="Search by user or seeker name"),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    x_admin_key: Optional[str] = Header(None)
):
    """Retrieve full Kundli generation history with timestamps and birth parameters."""
    verify_admin(x_admin_key)
    records = get_all_records(search=search, limit=limit, offset=offset)
    return {"records": records, "count": len(records)}


@router.post("/users/{user_id}/limit")
def api_adjust_user_limit(
    user_id: str,
    req: AdjustLimitRequest,
    x_admin_key: Optional[str] = Header(None)
):
    """Admin can reset checks used or grant additional limits for a user."""
    verify_admin(x_admin_key)
    try:
        updated = adjust_user_limit(user_id, new_limit=req.new_limit, reset_checks=req.reset_checks)
        return {"status": "success", "user": updated}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

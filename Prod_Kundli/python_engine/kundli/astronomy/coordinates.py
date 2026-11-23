"""Geographic coordinates, time conversions, and birth input model."""
from datetime import datetime
from datetime import date as dt_date
from datetime import time as dt_time
from typing import Optional, Literal
from pydantic import BaseModel, Field, field_validator
import pytz


class BirthInput(BaseModel):
    # User Contact Information (for 10-check limit & Admin audit)
    user_name: Optional[str] = Field(default=None, description="User full name")
    user_email: Optional[str] = Field(default=None, description="User email for limit enforcement")
    user_mobile: Optional[str] = Field(default=None, description="User mobile number")

    # Native / Seeker Birth Information
    name: str = Field(default="Seeker", description="Name of the person / chart native")
    date: dt_date = Field(..., description="Birth date in YYYY-MM-DD")
    time: dt_time = Field(..., description="Birth time in HH:MM:SS")
    timezone: str = Field(default="Asia/Kolkata", description="IANA timezone identifier")
    latitude: float = Field(..., ge=-90.0, le=90.0, description="Latitude in decimal degrees (-90 to +90)")
    longitude: float = Field(..., ge=-180.0, le=180.0, description="Longitude in decimal degrees (-180 to +180)")
    altitude: float = Field(default=0.0, description="Altitude in meters")
    ayanamsa: str = Field(default="Lahiri", description="Ayanamsa system: Lahiri, KP, Raman, etc.")
    node_type: Literal["mean", "true"] = Field(default="mean", description="Rahu/Ketu calculation mode")
    house_system: str = Field(default="P", description="P for Placidus, W for Whole Sign, E for Equal, S for Sripati")
    chart_type: str = Field(default="vedic", description="vedic or kp")

    @field_validator("timezone")
    @classmethod
    def validate_tz(cls, v: str) -> str:
        try:
            pytz.timezone(v)
            return v
        except Exception:
            raise ValueError(f"Invalid timezone: {v}. Must be a valid IANA timezone like 'Asia/Kolkata', 'UTC', etc.")


def to_utc_datetime(birth_date: dt_date, birth_time: dt_time, tz_name: str) -> datetime:
    """Convert local date and time in given timezone to UTC datetime."""
    tz = pytz.timezone(tz_name)
    local_dt = datetime.combine(birth_date, birth_time)
    localized = tz.localize(local_dt)
    return localized.astimezone(pytz.utc)


def decimal_hour(dt: datetime) -> float:
    """Return hour as decimal (e.g. 14:35:00 -> 14 + 35/60 = 14.5833)."""
    return dt.hour + dt.minute / 60.0 + dt.second / 3600.0 + dt.microsecond / 3.6e9

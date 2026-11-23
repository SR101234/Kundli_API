"""Swiss Ephemeris wrapper and Julian Day calculations."""
import os
from datetime import datetime
import swisseph as swe


# Setup Swiss Ephemeris data path if available, or use built-in Moshier ephemeris
EPHE_PATH = os.environ.get("SE_EPHE_PATH", "")
swe.set_ephe_path(EPHE_PATH)


def calculate_julian_day(utc_dt: datetime) -> float:
    """Calculate Julian Day in Universal Time (UT1/UTC) from UTC datetime."""
    decimal_h = utc_dt.hour + utc_dt.minute / 60.0 + utc_dt.second / 3600.0 + utc_dt.microsecond / 3.6e9
    return float(swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, decimal_h))


def calculate_sidereal_time(tjd_ut: float) -> float:
    """Calculate Greenwich Mean Sidereal Time in hours."""
    return float(swe.sidtime(tjd_ut))

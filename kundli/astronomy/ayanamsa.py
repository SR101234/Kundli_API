"""Ayanamsa configuration and mapping for Swiss Ephemeris."""
from enum import Enum
import swisseph as swe


class AyanamsaType(str, Enum):
    LAHIRI = "Lahiri"
    KRISHNAMURTI = "KP"
    KRISHNAMURTI_VP = "KP_VP"
    RAMAN = "Raman"
    FAGAN_BRADLEY = "Fagan_Bradley"
    DELUCE = "DeLuce"
    YUKTESHWAR = "Yukteshwar"
    TRUE_CITRA = "True_Citra"
    SAYANA = "Sayana"  # Tropical / 0 ayanamsa


AYANAMSA_MAP = {
    AyanamsaType.LAHIRI: swe.SIDM_LAHIRI,
    AyanamsaType.KRISHNAMURTI: swe.SIDM_KRISHNAMURTI,
    AyanamsaType.KRISHNAMURTI_VP: getattr(swe, "SIDM_KRISHNAMURTI_VP291", swe.SIDM_KRISHNAMURTI),
    AyanamsaType.RAMAN: swe.SIDM_RAMAN,
    AyanamsaType.FAGAN_BRADLEY: swe.SIDM_FAGAN_BRADLEY,
    AyanamsaType.DELUCE: swe.SIDM_DELUCE,
    AyanamsaType.YUKTESHWAR: swe.SIDM_YUKTESHWAR,
    AyanamsaType.TRUE_CITRA: swe.SIDM_TRUE_CITRA,
}


def configure_ayanamsa(ayanamsa_name: str) -> int:
    """Set the sidereal calculation mode in Swiss Ephemeris."""
    matched = None
    for item in AyanamsaType:
        if item.value.lower() == ayanamsa_name.lower() or item.name.lower() == ayanamsa_name.lower():
            matched = item
            break
    if not matched:
        matched = AyanamsaType.LAHIRI

    if matched == AyanamsaType.SAYANA:
        return -1  # Sayana / Tropical

    sid_mode = AYANAMSA_MAP[matched]
    swe.set_sid_mode(sid_mode)
    return sid_mode


def get_ayanamsa_value(tjd_ut: float, ayanamsa_name: str = "Lahiri") -> float:
    """Return the exact ayanamsa degree for a given Julian Day UT."""
    configure_ayanamsa(ayanamsa_name)
    if ayanamsa_name.lower() in ("sayana", "tropical"):
        return 0.0
    return float(swe.get_ayanamsa_ut(tjd_ut))

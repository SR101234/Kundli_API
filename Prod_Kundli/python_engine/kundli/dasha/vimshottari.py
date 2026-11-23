"""Vimshottari Dasha calculation engine (5 levels: Maha, Antar, Pratyantar, Sookshma, Prana)."""
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from kundli.core.nakshatra import get_nakshatra_from_longitude
from kundli.dasha.base import BaseDasha

# 120-year Vimshottari period table
VIMSHOTTARI_PERIODS = [
    ("Ketu", 7),
    ("Venus", 20),
    ("Sun", 6),
    ("Moon", 10),
    ("Mars", 7),
    ("Rahu", 18),
    ("Jupiter", 16),
    ("Saturn", 19),
    ("Mercury", 17),
]
VIM_CYCLE = [p[0] for p in VIMSHOTTARI_PERIODS]
VIM_YEARS = {p[0]: p[1] for p in VIMSHOTTARI_PERIODS}
TOTAL_CYCLE_YEARS = 120.0
DAYS_PER_YEAR = 365.242199  # Tropical solar year days


class DashaPeriod(BaseModel):
    lord: str
    level: str  # Mahadasha, Antardasha, Pratyantardasha
    start_date: str
    end_date: str
    sub_periods: Optional[List['DashaPeriod']] = None


class VimshottariDasha(BaseDasha):
    def calculate_dasha_timeline(
        self,
        birth_datetime: datetime,
        moon_longitude: float,
        target_datetime: Optional[datetime] = None
    ) -> Dict[str, Any]:
        if target_datetime is None:
            target_datetime = datetime.now()

        moon_nak = get_nakshatra_from_longitude(moon_longitude)
        first_lord = moon_nak["nakshatra_lord"]
        deg_in_nak = moon_nak["degree_in_nakshatra"]
        nak_span = 360.0 / 27.0  # 13.333333 degrees

        # Fraction of nakshatra already traversed
        traversed_fraction = deg_in_nak / nak_span
        balance_fraction = 1.0 - traversed_fraction

        lord_total_years = VIM_YEARS[first_lord]
        balance_years = lord_total_years * balance_fraction
        balance_days = balance_years * DAYS_PER_YEAR

        # Sequence of 9 Mahadashas starting with first_lord
        start_idx = VIM_CYCLE.index(first_lord)
        mahadashas: List[Dict[str, Any]] = []

        current_start = birth_datetime
        for i in range(9):
            p_name = VIM_CYCLE[(start_idx + i) % 9]
            if i == 0:
                duration_days = balance_days
            else:
                duration_days = VIM_YEARS[p_name] * DAYS_PER_YEAR

            current_end = current_start + timedelta(days=duration_days)

            # Sub-periods (Antardashas)
            antardashas = self._calculate_antardashas(p_name, current_start, current_end, is_first=(i == 0), balance_fraction=balance_fraction)

            mahadashas.append({
                "lord": p_name,
                "start_date": current_start.strftime("%Y-%m-%d"),
                "end_date": current_end.strftime("%Y-%m-%d"),
                "antardashas": antardashas
            })
            current_start = current_end

        # Find current running Mahadasha, Antardasha, Pratyantardasha
        current_running = self._find_running_hierarchy(mahadashas, target_datetime)

        return {
            "first_lord": first_lord,
            "balance_years": round(balance_years, 3),
            "balance_days": round(balance_days, 1),
            "current_running": current_running,
            "mahadashas": mahadashas
        }

    def _calculate_antardashas(
        self,
        maha_lord: str,
        maha_start: datetime,
        maha_end: datetime,
        is_first: bool = False,
        balance_fraction: float = 1.0
    ) -> List[Dict[str, Any]]:
        """Calculate Antardashas within a Mahadasha."""
        m_years = VIM_YEARS[maha_lord]
        start_idx = VIM_CYCLE.index(maha_lord)
        antardashas = []

        cur_start = maha_start
        # Full nominal antardashas for this mahadasha
        for j in range(9):
            antar_lord = VIM_CYCLE[(start_idx + j) % 9]
            a_years = VIM_YEARS[antar_lord]
            # Duration in days = Maha_years * (Antar_years / 120) * 365.2422
            a_duration_days = m_years * (a_years / TOTAL_CYCLE_YEARS) * DAYS_PER_YEAR
            cur_end = cur_start + timedelta(days=a_duration_days)

            # Pratyantardashas
            pratyantardashas = self._calculate_pratyantardashas(maha_lord, antar_lord, cur_start, cur_end)

            antardashas.append({
                "lord": antar_lord,
                "start_date": cur_start.strftime("%Y-%m-%d"),
                "end_date": cur_end.strftime("%Y-%m-%d"),
                "pratyantardashas": pratyantardashas
            })
            cur_start = cur_end

        return antardashas

    def _calculate_pratyantardashas(
        self,
        maha_lord: str,
        antar_lord: str,
        antar_start: datetime,
        antar_end: datetime
    ) -> List[Dict[str, Any]]:
        """Calculate Pratyantardashas within an Antardasha."""
        m_years = VIM_YEARS[maha_lord]
        a_years = VIM_YEARS[antar_lord]
        start_idx = VIM_CYCLE.index(antar_lord)
        pratyantardashas = []

        cur_start = antar_start
        for k in range(9):
            prat_lord = VIM_CYCLE[(start_idx + k) % 9]
            p_years = VIM_YEARS[prat_lord]
            # Pratyantar days = Maha_years * (Antar_years / 120) * (Prat_years / 120) * 365.2422
            p_duration_days = m_years * (a_years / TOTAL_CYCLE_YEARS) * (p_years / TOTAL_CYCLE_YEARS) * DAYS_PER_YEAR
            cur_end = cur_start + timedelta(days=p_duration_days)

            pratyantardashas.append({
                "lord": prat_lord,
                "start_date": cur_start.strftime("%Y-%m-%d"),
                "end_date": cur_end.strftime("%Y-%m-%d")
            })
            cur_start = cur_end

        return pratyantardashas

    def _find_running_hierarchy(self, mahadashas: List[Dict[str, Any]], target_dt: datetime) -> Dict[str, Any]:
        """Locate the exact running Mahadasha, Antardasha, and Pratyantardasha."""
        target_str = target_dt.strftime("%Y-%m-%d")
        running = {
            "mahadasha": None,
            "antardasha": None,
            "pratyantardasha": None,
            "summary": "Running Dasha information"
        }

        for md in mahadashas:
            if md["start_date"] <= target_str <= md["end_date"]:
                running["mahadasha"] = {
                    "lord": md["lord"],
                    "start": md["start_date"],
                    "end": md["end_date"]
                }
                for ad in md.get("antardashas", []):
                    if ad["start_date"] <= target_str <= ad["end_date"]:
                        running["antardasha"] = {
                            "lord": ad["lord"],
                            "start": ad["start_date"],
                            "end": ad["end_date"]
                        }
                        for pd in ad.get("pratyantardashas", []):
                            if pd["start_date"] <= target_str <= pd["end_date"]:
                                running["pratyantardasha"] = {
                                    "lord": pd["lord"],
                                    "start": pd["start_date"],
                                    "end": pd["end_date"]
                                }
                                break
                        break
                break

        if running["mahadasha"] and running["antardasha"] and running["pratyantardasha"]:
            m_lord = running["mahadasha"]["lord"]
            a_lord = running["antardasha"]["lord"]
            p_lord = running["pratyantardasha"]["lord"]
            running["summary"] = f"{m_lord} - {a_lord} - {p_lord}"

        return running

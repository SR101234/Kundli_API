"""House cusps, Ascendant (Lagna), and house placements calculation."""
from typing import Dict, Any, List, Tuple
import swisseph as swe
from pydantic import BaseModel
from kundli.astronomy.ayanamsa import configure_ayanamsa
from kundli.core.zodiac import get_sign_from_longitude
from kundli.core.nakshatra import get_nakshatra_from_longitude
from kundli.astronomy.planets import PlanetPosition


class HouseCusp(BaseModel):
    house: int
    longitude: float
    sign: str
    sign_index: int
    sign_lord: str
    degree_in_sign: float
    nakshatra: str
    nakshatra_lord: str
    nakshatra_pada: int
    start_longitude: float = 0.0
    end_longitude: float = 0.0


class HouseCalculationResult(BaseModel):
    ascendant: PlanetPosition
    midheaven: PlanetPosition
    houses: List[HouseCusp]
    house_system: str
    ayanamsa_value: float


def calculate_houses_and_ascendant(
    tjd_ut: float,
    latitude: float,
    longitude: float,
    ayanamsa_name: str = "Lahiri",
    house_system: str = "P"
) -> HouseCalculationResult:
    """Calculate 12 house cusps and Ascendant/MC with given house system."""
    sid_mode = configure_ayanamsa(ayanamsa_name)
    hsys = house_system.encode("ascii") if isinstance(house_system, str) else house_system

    # swe.houses_ex with sidereal flag gives sidereal houses directly
    flag = swe.FLG_SWIEPH
    if sid_mode != -1:
        flag |= swe.FLG_SIDEREAL

    cusps, ascmc = swe.houses_ex(tjd_ut, latitude, longitude, hsys, flag)
    asc_lon = ascmc[0] % 360.0
    mc_lon = ascmc[1] % 360.0

    asc_sign = get_sign_from_longitude(asc_lon)
    asc_nak = get_nakshatra_from_longitude(asc_lon)

    ascendant_pos = PlanetPosition(
        planet="Ascendant",
        longitude=round(asc_lon, 4),
        latitude=0.0,
        speed=0.0,
        retrograde=False,
        sign=asc_sign["sign"],
        sign_index=asc_sign["sign_index"],
        sign_lord=asc_sign["sign_lord"],
        degree_in_sign=round(asc_sign["degree_in_sign"], 4),
        nakshatra=asc_nak["nakshatra"],
        nakshatra_index=asc_nak["nakshatra_index"],
        nakshatra_lord=asc_nak["nakshatra_lord"],
        nakshatra_pada=asc_nak["nakshatra_pada"],
        house=1
    )

    mc_sign = get_sign_from_longitude(mc_lon)
    mc_nak = get_nakshatra_from_longitude(mc_lon)

    midheaven_pos = PlanetPosition(
        planet="Midheaven",
        longitude=round(mc_lon, 4),
        latitude=0.0,
        speed=0.0,
        retrograde=False,
        sign=mc_sign["sign"],
        sign_index=mc_sign["sign_index"],
        sign_lord=mc_sign["sign_lord"],
        degree_in_sign=round(mc_sign["degree_in_sign"], 4),
        nakshatra=mc_nak["nakshatra"],
        nakshatra_index=mc_nak["nakshatra_index"],
        nakshatra_lord=mc_nak["nakshatra_lord"],
        nakshatra_pada=mc_nak["nakshatra_pada"],
        house=10
    )

    house_list: List[HouseCusp] = []
    # In pyswisseph, cusps has length 12 (index 0 is House 1, index 11 is House 12)
    for i in range(12):
        house_num = i + 1
        h_lon = cusps[i] % 360.0
        h_sign = get_sign_from_longitude(h_lon)
        h_nak = get_nakshatra_from_longitude(h_lon)
        
        # Calculate house start and end span
        prev_idx = 11 if i == 0 else i - 1
        next_idx = 0 if i == 11 else i + 1
        
        # Midpoint with previous cusp is house start
        prev_lon = cusps[prev_idx] % 360.0
        diff_prev = (h_lon - prev_lon) % 360.0
        start_lon = (prev_lon + diff_prev / 2.0) % 360.0
        
        # Midpoint with next cusp is house end
        next_lon = cusps[next_idx] % 360.0
        diff_next = (next_lon - h_lon) % 360.0
        end_lon = (h_lon + diff_next / 2.0) % 360.0

        house_list.append(HouseCusp(
            house=house_num,
            longitude=round(h_lon, 4),
            sign=h_sign["sign"],
            sign_index=h_sign["sign_index"],
            sign_lord=h_sign["sign_lord"],
            degree_in_sign=round(h_sign["degree_in_sign"], 4),
            nakshatra=h_nak["nakshatra"],
            nakshatra_lord=h_nak["nakshatra_lord"],
            nakshatra_pada=h_nak["nakshatra_pada"],
            start_longitude=round(start_lon, 4),
            end_longitude=round(end_lon, 4)
        ))

    ayanamsa_val = swe.get_ayanamsa_ut(tjd_ut) if sid_mode != -1 else 0.0

    return HouseCalculationResult(
        ascendant=ascendant_pos,
        midheaven=midheaven_pos,
        houses=house_list,
        house_system=house_system,
        ayanamsa_value=round(ayanamsa_val, 4)
    )


def assign_houses_to_planets(
    planets: Dict[str, PlanetPosition],
    ascendant_sign_index: int,
    house_cusps: List[HouseCusp]
) -> None:
    """Assign Rashi-based house and Bhava Chalit house to each planet."""
    for p_name, p in planets.items():
        # Vedic Rashi Chart (Whole Sign from Ascendant)
        # House 1 = Ascendant sign, House 2 = Ascendant sign + 1, etc.
        rashi_house = ((p.sign_index - ascendant_sign_index) % 12) + 1
        p.house = rashi_house

        # Bhava Chalit (Cuspal house placement based on sandhi midpoints)
        chalit_house = rashi_house  # Default fallback
        for h in house_cusps:
            # Check if planet longitude falls in [start_longitude, end_longitude)
            start = h.start_longitude
            end = h.end_longitude
            p_lon = p.longitude
            
            in_house = False
            if start <= end:
                in_house = (start <= p_lon < end)
            else:
                # Wraps across 0 Aries
                in_house = (p_lon >= start or p_lon < end)
            
            if in_house:
                chalit_house = h.house
                break
        p.bhava_chalit_house = chalit_house

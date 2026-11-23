"""Chart renderers for North Indian, South Indian, and East Indian formats."""
from typing import Dict, Any, List

# North Indian chart house geometry (12 diamond/triangular houses)
# 1st house is top diamond, 2nd top-left triangle, 4th left diamond, 7th bottom diamond, 10th right diamond.

def render_north_indian_svg(house_signs: Dict[int, str], house_planets: Dict[int, List[Any]], width: int = 500, height: int = 500) -> str:
    """Generate SVG string for a traditional North Indian diamond chart."""
    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" style="background:#fffcf7; font-family:system-ui, -apple-system, sans-serif;">',
        # Outer border
        f'<rect x="12" y="12" width="{width-24}" height="{height-24}" rx="8" fill="#fffcf7" stroke="#92400e" stroke-width="2.5"/>',
        # Diagonals
        f'<line x1="12" y1="12" x2="{width-12}" y2="{height-12}" stroke="#b45309" stroke-width="1.8"/>',
        f'<line x1="{width-12}" y1="12" x2="12" y2="{height-12}" stroke="#b45309" stroke-width="1.8"/>',
        # Center diamond lines
        f'<line x1="{width//2}" y1="12" x2="12" y2="{height//2}" stroke="#b45309" stroke-width="1.8"/>',
        f'<line x1="12" y1="{height//2}" x2="{width//2}" y2="{height-12}" stroke="#b45309" stroke-width="1.8"/>',
        f'<line x1="{width//2}" y1="{height-12}" x2="{width-12}" y2="{height//2}" stroke="#b45309" stroke-width="1.8"/>',
        f'<line x1="{width-12}" y1="{height//2}" x2="{width//2}" y2="12" stroke="#b45309" stroke-width="1.8"/>',
    ]

    # Center coordinates for each of the 12 houses in North Indian diamond layout
    house_coords = {
        1: (width * 0.50, height * 0.28),
        2: (width * 0.25, height * 0.16),
        3: (width * 0.14, height * 0.28),
        4: (width * 0.28, height * 0.50),
        5: (width * 0.14, height * 0.72),
        6: (width * 0.25, height * 0.84),
        7: (width * 0.50, height * 0.72),
        8: (width * 0.75, height * 0.84),
        9: (width * 0.86, height * 0.72),
        10: (width * 0.72, height * 0.50),
        11: (width * 0.86, height * 0.28),
        12: (width * 0.75, height * 0.16),
    }

    # Add house numbers / sign names and planet labels
    for h, (cx, cy) in house_coords.items():
        sign_str = house_signs.get(h, "")
        # Header: Sign name + house
        svg_parts.append(f'<text x="{cx}" y="{cy - 14}" font-size="11.5" font-weight="700" fill="#78350f" text-anchor="middle">{sign_str} ({h})</text>')
        
        planets_in_h = house_planets.get(h, [])
        p_names = []
        for p in planets_in_h:
            if isinstance(p, dict):
                p_text = p.get("planet", "")
                if p.get("retrograde"): p_text += " (R)"
                if p.get("is_combust"): p_text += " (C)"
                p_names.append(p_text)
            else:
                p_names.append(str(p))

        y_offset = cy + 3
        for name in p_names[:4]:
            color = "#c2410c" if "(R)" in name else "#1e3a8a"
            svg_parts.append(f'<text x="{cx}" y="{y_offset}" font-size="10.5" font-weight="700" fill="{color}" text-anchor="middle">{name}</text>')
            y_offset += 13.5

    svg_parts.append('</svg>')
    return "\n".join(svg_parts)
    return "\n".join(svg_parts)


def render_south_indian_svg(house_signs: Dict[int, str], house_planets: Dict[int, List[Any]], width: int = 500, height: int = 500) -> str:
    """Generate SVG string for a traditional South Indian square box chart."""
    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" style="background:#fffaf0; font-family:sans-serif;">',
        f'<rect x="10" y="10" width="{width-20}" height="{height-20}" fill="none" stroke="#b45309" stroke-width="3"/>',
    ]

    cell_w = (width - 20) / 4.0
    cell_h = (height - 20) / 4.0

    # Grid lines
    for i in range(1, 4):
        svg_parts.append(f'<line x1="{10 + i * cell_w}" y1="10" x2="{10 + i * cell_w}" y2="{height-10}" stroke="#b45309" stroke-width="1.5"/>')
        svg_parts.append(f'<line x1="10" y1="{10 + i * cell_h}" x2="{width-10}" y2="{10 + i * cell_h}" stroke="#b45309" stroke-width="1.5"/>')

    # Center 2x2 box filled blank
    svg_parts.append(f'<rect x="{10 + cell_w}" y="{10 + cell_h}" width="{cell_w * 2}" height="{cell_h * 2}" fill="#fef3c7" stroke="#b45309" stroke-width="2"/>')
    svg_parts.append(f'<text x="{width/2}" y="{height/2}" font-size="14" font-weight="bold" fill="#92400e" text-anchor="middle">South Indian Kundli</text>')

    # South Indian signs are fixed in position:
    # Top row: Pisces (0,0), Aries (1,0), Taurus (2,0), Gemini (3,0)
    # Right col: Cancer (3,1), Leo (3,2)
    # Bottom row: Virgo (3,3), Libra (2,3), Scorpio (1,3), Sagittarius (0,3)
    # Left col: Capricorn (0,2), Aquarius (0,1)
    # Map each sign to grid cell (col, row)
    sign_grid_pos = {
        "Pisces": (0, 0), "Aries": (1, 0), "Taurus": (2, 0), "Gemini": (3, 0),
        "Cancer": (3, 1), "Leo": (3, 2), "Virgo": (3, 3),
        "Libra": (2, 3), "Scorpio": (1, 3), "Sagittarius": (0, 3),
        "Capricorn": (0, 2), "Aquarius": (0, 1)
    }

    # Render each sign's box
    for sign_name, (c, r) in sign_grid_pos.items():
        bx = 10 + c * cell_w
        by = 10 + r * cell_h
        # Find which house has this sign
        house_num = next((h for h, s in house_signs.items() if s == sign_name), None)
        header = f"{sign_name}" + (f" (H{house_num})" if house_num else "")
        svg_parts.append(f'<text x="{bx + 6}" y="{by + 16}" font-size="10" font-weight="bold" fill="#78350f">{header}</text>')
        
        if house_num:
            planets_in_h = house_planets.get(house_num, [])
            py = by + 32
            for p in planets_in_h:
                p_text = p.get("planet", "") if isinstance(p, dict) else str(p)
                svg_parts.append(f'<text x="{bx + 6}" y="{py}" font-size="10" font-weight="600" fill="#1e3a8a">{p_text}</text>')
                py += 14

    svg_parts.append('</svg>')
    return "\n".join(svg_parts)

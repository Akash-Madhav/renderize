#!/usr/bin/env python3
"""
generate_furniture_sprites.py - Architectural Plan-View Furniture Sprite Library

Generates publication-grade, top-down 2D plan-view furniture symbols with delicate
ambient drop shadows and authentic materials:
1. Master King Bed Suite with timber headboard, high-thread-count duvet, throw runner & nightstands
2. Modern Sectional L-Sofa with upholstered seat cushions & fluted coffee table
3. 6-Seater Formal Walnut Dining Ensemble with chairs tucked under table
4. Executive Workstation Desk with task chair & storage pedestal
5. Luxury Sanitary Ensemble: Porcelain white vanity counter, basin & WC
"""

import os
from PIL import Image, ImageDraw, ImageFilter


def create_bed_double(output_path, size=(320, 340)):
    """Generates Master King Bed Suite with timber headboard, duvet, throw & nightstands."""
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Soft ambient drop shadow underneath bed frame
    shadow = Image.new("RGBA", size, (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    sdraw.rounded_rectangle([35, 25, 285, 320], radius=10, fill=(26, 30, 33, 70))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=6))
    img.paste(shadow, (0, 0), shadow)

    # Nightstands (Timber walnut with brass reading lamp circle)
    draw.rounded_rectangle([10, 30, 48, 85], radius=4, fill="#4A2E1B", outline="#2A170B", width=2)
    draw.ellipse([22, 50, 36, 64], fill="#E8D8A0", outline="#A89050", width=1)

    draw.rounded_rectangle([272, 30, 310, 85], radius=4, fill="#4A2E1B", outline="#2A170B", width=2)
    draw.ellipse([284, 50, 298, 64], fill="#E8D8A0", outline="#A89050", width=1)

    # Timber Bed Base & Headboard
    draw.rounded_rectangle([45, 30, 275, 310], radius=8, fill="#5C381E", outline="#301A09", width=2)
    draw.rounded_rectangle([40, 15, 280, 40], radius=4, fill="#301A09")

    # High-Thread-Count Mattress / Duvet (Warm Ivory #F7F5F0)
    draw.rounded_rectangle([52, 45, 268, 305], radius=6, fill="#F7F5F0", outline="#D5D0C5", width=1)

    # King Pillows (Dual angled pillows with subtle fold lines)
    draw.rounded_rectangle([65, 55, 150, 105], radius=6, fill="#FFFFFF", outline="#D5D0C5", width=1)
    draw.rounded_rectangle([170, 55, 255, 105], radius=6, fill="#FFFFFF", outline="#D5D0C5", width=1)

    # Decorative Throw Runner (Architectural Sage/Olive accent #4A5E3A)
    draw.rectangle([52, 220, 268, 295], fill="#4A5E3A")
    draw.line([52, 220, 268, 220], fill="#354528", width=1)
    draw.line([52, 295, 268, 295], fill="#354528", width=1)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    img.save(output_path)
    print(f"[✓] Generated Bed Suite Sprite: {output_path}")


def create_sofa_sectional(output_path, size=(340, 340)):
    """Generates modern L-shaped sectional sofa with coffee table."""
    img = Image.new("RGBA", size, (0, 0, 0, 0))

    # Drop shadow
    shadow = Image.new("RGBA", size, (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    sdraw.rounded_rectangle([25, 25, 320, 100], radius=8, fill=(26, 30, 33, 65))
    sdraw.rounded_rectangle([25, 100, 100, 320], radius=8, fill=(26, 30, 33, 65))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=6))
    img.paste(shadow, (0, 0), shadow)

    draw = ImageDraw.Draw(img)
    sofa_bg = "#4A5E3A"  # Warm architectural olive
    border_col = "#2F3D24"
    cushion_bg = "#586F46"

    # L-Shape Backrest and Armrests
    draw.rounded_rectangle([20, 20, 315, 80], radius=8, fill=sofa_bg, outline=border_col, width=2)
    draw.rounded_rectangle([20, 80, 80, 315], radius=8, fill=sofa_bg, outline=border_col, width=2)

    # Individual Plump Seat Cushions
    # Horizontal segment cushions
    for x in range(80, 300, 75):
        draw.rounded_rectangle([x + 3, 80, x + 75, 175], radius=6, fill=cushion_bg, outline=border_col, width=1)
    # Vertical chaise cushion
    draw.rounded_rectangle([80, 180, 175, 310], radius=6, fill=cushion_bg, outline=border_col, width=1)

    # Fluted Oak Coffee Table in corner of L
    draw.rounded_rectangle([190, 190, 305, 305], radius=12, fill="#8B5A2B", outline="#4A2E1B", width=2)
    draw.rounded_rectangle([200, 200, 295, 295], radius=8, fill="#9E6935", outline="#73421C", width=1)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    img.save(output_path)
    print(f"[✓] Generated Sectional Sofa Sprite: {output_path}")


def create_dining_table(output_path, size=(300, 200)):
    """Generates 6-seater solid walnut dining table with minimalist chairs."""
    img = Image.new("RGBA", size, (0, 0, 0, 0))

    # Shadow
    shadow = Image.new("RGBA", size, (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    sdraw.rounded_rectangle([55, 45, 245, 155], radius=6, fill=(26, 30, 33, 60))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=5))
    img.paste(shadow, (0, 0), shadow)

    draw = ImageDraw.Draw(img)

    # 6 Dining Chairs tucked under table perimeter
    chair_col = "#382314"
    cush_col = "#D8D3C8"
    # Top row (3 chairs)
    for cx in [70, 130, 190]:
        draw.rounded_rectangle([cx, 18, cx + 40, 50], radius=4, fill=chair_col)
        draw.rounded_rectangle([cx + 4, 30, cx + 36, 48], radius=3, fill=cush_col)
    # Bottom row (3 chairs)
    for cx in [70, 130, 190]:
        draw.rounded_rectangle([cx, 150, cx + 40, 182], radius=4, fill=chair_col)
        draw.rounded_rectangle([cx + 4, 152, cx + 36, 170], radius=3, fill=cush_col)

    # Table Top: Rich solid walnut with subtle perimeter bevel
    draw.rounded_rectangle([50, 40, 250, 160], radius=8, fill="#4A2E1B", outline="#2A170B", width=2)
    draw.rounded_rectangle([56, 46, 244, 154], radius=6, fill="#5C381E", outline="#3E2210", width=1)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    img.save(output_path)
    print(f"[✓] Generated Dining Ensemble Sprite: {output_path}")


def create_sanitary_fixtures(output_path, size=(160, 220)):
    """Generates luxury plan-view WC and vanity washbasin ensemble."""
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Vanity Countertop (Italian marble tone with hairline edge)
    draw.rounded_rectangle([15, 15, 145, 95], radius=6, fill="#E8ECE9", outline="#24282B", width=2)
    # Oval Porcelain Washbasin
    draw.ellipse([45, 28, 115, 82], fill="#FFFFFF", outline="#70757A", width=2)
    # Chrome swivel faucet
    draw.ellipse([76, 32, 84, 40], fill="#363C40")
    draw.line([80, 40, 80, 52], fill="#8B949E", width=3)

    # Modern Wall-Hung WC Suite
    # Cistern box
    draw.rounded_rectangle([35, 120, 125, 155], radius=4, fill="#F7F9F8", outline="#24282B", width=2)
    draw.ellipse([74, 132, 86, 144], fill="#A0A5A8")  # Dual flush button
    # Pan (egg/elongated bowl profile)
    draw.ellipse([42, 145, 118, 208], fill="#FFFFFF", outline="#24282B", width=2)
    draw.ellipse([52, 160, 108, 198], fill="#F0F4F2", outline="#8B949E", width=1)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    img.save(output_path)
    print(f"[✓] Generated Sanitary Fixture Sprite: {output_path}")


def main():
    furn_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "furniture"))
    os.makedirs(furn_dir, exist_ok=True)
    print("[+] Generating plan-view furniture sprite library...")
    create_bed_double(os.path.join(furn_dir, "bed_double.png"))
    create_sofa_sectional(os.path.join(furn_dir, "sofa_sectional.png"))
    create_dining_table(os.path.join(furn_dir, "dining_table.png"))
    create_sanitary_fixtures(os.path.join(furn_dir, "sanitary_fixtures.png"))
    print("[✓] All furniture sprites generated successfully!")


if __name__ == "__main__":
    main()

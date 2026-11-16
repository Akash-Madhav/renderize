#!/usr/bin/env python3
"""
generate_furniture_sprites.py - Plan-View Furniture Sprites

Generates 2D top-down plan-view furniture symbols:
1. Double Bed with wooden headboard & bedside nightstands
2. L-shaped Sectional Sofa in olive upholstery
3. Dining Table with 6 chairs
4. Office Workstation Desk
5. Bathroom Vanity & Toilet fixture
"""

import os
from PIL import Image, ImageDraw


def create_bed_double(output_path, size=(240, 260)):
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Bed base / timber frame
    draw.rounded_rectangle([30, 20, 210, 240], radius=8, fill="#5A3A1E", outline="#3B2513", width=2)
    # Headboard
    draw.rounded_rectangle([25, 10, 215, 30], radius=4, fill="#3B2513")
    # Mattress / duvet (cream with decorative throw)
    draw.rounded_rectangle([35, 35, 205, 235], radius=6, fill="#EFEFEA", outline="#D0D0C8", width=1)
    # Pillows
    draw.rounded_rectangle([45, 45, 110, 85], radius=6, fill="#FFFFFF", outline="#D0D0C8", width=1)
    draw.rounded_rectangle([130, 45, 195, 85], radius=6, fill="#FFFFFF", outline="#D0D0C8", width=1)
    # Runner throw (olive accent)
    draw.rectangle([35, 170, 205, 230], fill="#4A5E3A")

    # Nightstands
    draw.rounded_rectangle([0, 20, 25, 65], radius=3, fill="#5A3A1E")
    draw.rounded_rectangle([215, 20, 240, 65], radius=3, fill="#5A3A1E")

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    img.save(output_path)
    print(f"[✓] Generated: {output_path}")


def create_sofa_sectional(output_path, size=(260, 260)):
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    sofa_color = "#5A6E4A"
    cushion_border = "#3B4A2F"

    # L-shape backrests
    draw.rounded_rectangle([10, 10, 250, 60], radius=6, fill=sofa_color, outline=cushion_border, width=2)
    draw.rounded_rectangle([10, 60, 60, 250], radius=6, fill=sofa_color, outline=cushion_border, width=2)
    # Seat cushions
    draw.rounded_rectangle([60, 60, 250, 150], radius=4, fill="#687E56", outline=cushion_border, width=1)
    draw.rounded_rectangle([60, 150, 150, 250], radius=4, fill="#687E56", outline=cushion_border, width=1)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    img.save(output_path)
    print(f"[✓] Generated: {output_path}")


def create_dining_table(output_path, size=(220, 150)):
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Tabletop
    draw.rounded_rectangle([40, 25, 180, 125], radius=8, fill="#4A2E14", outline="#2F1C0B", width=2)

    # 6 Chairs
    chair_color = "#3B2513"
    # Top chairs
    draw.rounded_rectangle([50, 5, 80, 25], radius=3, fill=chair_color)
    draw.rounded_rectangle([95, 5, 125, 25], radius=3, fill=chair_color)
    draw.rounded_rectangle([140, 5, 170, 25], radius=3, fill=chair_color)
    # Bottom chairs
    draw.rounded_rectangle([50, 125, 80, 145], radius=3, fill=chair_color)
    draw.rounded_rectangle([95, 125, 125, 145], radius=3, fill=chair_color)
    draw.rounded_rectangle([140, 125, 170, 145], radius=3, fill=chair_color)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    img.save(output_path)
    print(f"[✓] Generated: {output_path}")


def create_sanitary_fixtures(output_path, size=(120, 180)):
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Toilet Water Closet (top-down view)
    draw.rectangle([35, 10, 85, 35], fill="#FFFFFF", outline="#24282B", width=2)  # cistern tank
    draw.ellipse([37, 30, 83, 90], fill="#FFFFFF", outline="#24282B", width=2)  # bowl

    # Basin
    draw.rounded_rectangle([25, 115, 95, 165], radius=8, fill="#FFFFFF", outline="#24282B", width=2)
    draw.ellipse([50, 130, 70, 150], outline="#24282B", width=1)
    draw.ellipse([58, 120, 62, 124], fill="#24282B")  # faucet tap

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    img.save(output_path)
    print(f"[✓] Generated: {output_path}")


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

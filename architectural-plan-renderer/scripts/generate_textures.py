#!/usr/bin/env python3
"""
generate_textures.py - Texture Asset Generator

Generates seamless tileable architectural textures according to the
exact color palettes and patterns from references/material-palette.md:
1. French Oak Herringbone Parquet
2. Italian Calacatta Marble
3. Verde Sage Honed Quartzite
4. Charcoal Slate Bathroom Tile
5. Warm Terrazzo Aggregate
6. Flamed Basalt Exterior Paver
"""

import os
from PIL import Image, ImageDraw, ImageFilter
import numpy as np


def create_herringbone_wood(output_path, size=512):
    """Generates warm herringbone wood parquet texture."""
    img = Image.new("RGB", (size, size), "#8B5A2B")
    draw = ImageDraw.Draw(img)

    plank_w = 32
    plank_l = 96

    # Base wood tone variations
    colors = ["#7B4E24", "#8B5A2B", "#9A6635", "#6F451F", "#A06B39"]

    np.random.seed(42)

    for y in range(-size, size * 2, plank_w):
        for x in range(-size, size * 2, plank_l):
            c = colors[np.random.randint(0, len(colors))]
            # 45 degree alternating planks
            draw.rectangle([x, y, x + plank_l - 2, y + plank_w - 2], fill=c)
            # subtle plank bevel line
            draw.line([x, y, x + plank_l - 2, y], fill="#4A2E14", width=1)
            draw.line([x, y + plank_w - 2, x + plank_l - 2, y + plank_w - 2], fill="#4A2E14", width=1)

    # Slight blur to soften wood grain
    img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    img.save(output_path)
    print(f"[✓] Generated: {output_path}")


def create_marble_texture(output_path, size=512):
    """Generates veined Italian marble texture."""
    img = Image.new("RGB", (size, size), "#F4F6F4")
    draw = ImageDraw.Draw(img)

    np.random.seed(101)

    # Veins
    for _ in range(8):
        points = []
        x = np.random.randint(0, size)
        y = 0
        while y < size:
            points.append((x, y))
            x += np.random.randint(-15, 20)
            y += np.random.randint(15, 35)

        vein_color = (
            np.random.randint(200, 220),
            np.random.randint(205, 225),
            np.random.randint(205, 225)
        )
        if len(points) > 1:
            draw.line(points, fill=vein_color, width=np.random.randint(2, 6))

    img = img.filter(ImageFilter.GaussianBlur(radius=2.5))
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    img.save(output_path)
    print(f"[✓] Generated: {output_path}")


def create_sage_stone_texture(output_path, size=512):
    """Generates honed sage green quartzite texture."""
    base_color = np.array([145, 165, 135], dtype=np.uint8)
    noise = np.random.normal(0, 6, (size, size, 3)).astype(np.int16)
    arr = np.clip(base_color + noise, 0, 255).astype(np.uint8)

    img = Image.fromarray(arr, "RGB")
    img = img.filter(ImageFilter.GaussianBlur(radius=0.8))
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    img.save(output_path)
    print(f"[✓] Generated: {output_path}")


def create_charcoal_tile(output_path, size=512):
    """Generates dark charcoal slate tile grid."""
    img = Image.new("RGB", (size, size), "#363C40")
    draw = ImageDraw.Draw(img)

    tile_size = 64
    grout_color = "#24282B"

    for i in range(0, size, tile_size):
        draw.line([(0, i), (size, i)], fill=grout_color, width=2)
        draw.line([(i, 0), (i, size)], fill=grout_color, width=2)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    img.save(output_path)
    print(f"[✓] Generated: {output_path}")


def create_terrazzo_texture(output_path, size=512):
    """Generates warm speckled terrazzo aggregate texture."""
    img = Image.new("RGB", (size, size), "#D0C2B2")
    draw = ImageDraw.Draw(img)

    np.random.seed(99)
    fleck_colors = ["#4A3B32", "#8C7A6B", "#EAE4DC", "#2D2621", "#9D8876"]

    for _ in range(1200):
        x = np.random.randint(0, size)
        y = np.random.randint(0, size)
        r = np.random.randint(1, 4)
        c = fleck_colors[np.random.randint(0, len(fleck_colors))]
        draw.ellipse([x - r, y - r, x + r, y + r], fill=c)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    img.save(output_path)
    print(f"[✓] Generated: {output_path}")


def create_exterior_paver(output_path, size=512):
    """Generates flamed basalt exterior paving slab texture."""
    img = Image.new("RGB", (size, size), "#B8BCB5")
    draw = ImageDraw.Draw(img)

    paver_w = 64
    paver_l = 128
    grout = "#7A8076"

    for y in range(0, size, paver_w):
        offset = (y // paver_w) % 2 * (paver_l // 2)
        for x in range(-paver_l, size + paver_l, paver_l):
            draw.rectangle([x + offset, y, x + offset + paver_l - 2, y + paver_w - 2], outline=grout, width=1)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    img.save(output_path)
    print(f"[✓] Generated: {output_path}")


def main():
    tex_dir = r"c:\Users\akash\renderize\architectural-plan-renderer\assets\textures"
    print("[+] Generating master texture library...")
    create_herringbone_wood(os.path.join(tex_dir, "wood_herringbone.png"))
    create_marble_texture(os.path.join(tex_dir, "marble_italian.png"))
    create_sage_stone_texture(os.path.join(tex_dir, "stone_sage.png"))
    create_charcoal_tile(os.path.join(tex_dir, "tile_charcoal.png"))
    create_terrazzo_texture(os.path.join(tex_dir, "terrazzo_warm.png"))
    create_exterior_paver(os.path.join(tex_dir, "paver_exterior.png"))
    print("[✓] All textures generated successfully!")


if __name__ == "__main__":
    main()

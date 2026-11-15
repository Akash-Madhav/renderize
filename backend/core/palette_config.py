"""
palette_config.py - Material Palette & Color Swatches

Directly imports the reverse-engineered visual specifications
from architectural-plan-renderer/references/material-palette.md.
"""

# Structural Elements
CANVAS_BG = "#F7FBFE"
WALL_EXTERNAL = "#24282B"
WALL_INTERNAL = "#3A3E41"
WALL_SHADOW = "#1A1E21"
COLUMN_CAP_ACCENT = "#B8A040"
WINDOW_GLAZING_ACCENT = "#00B5B8"
DOOR_LEAF_WOOD = "#5A3A1E"

# Floor Materials
FLOOR_WOOD_PARQUET = "#8B5A2B"
FLOOR_MARBLE_ITALIAN = "#E0E5DF"
FLOOR_STONE_SAGE = "#8B9E7A"
FLOOR_TILE_CHARCOAL = "#363C40"
FLOOR_TERRAZZO = "#D0C2B2"
FLOOR_PAVER_EXTERIOR = "#B8BCB5"

# Material Mappings by Semantic Room Type
MATERIAL_MAPPING = {
    "BEDROOM": {
        "material_name": "French Oak Herringbone Parquet",
        "texture_file": "wood_herringbone.png",
        "fallback_color": FLOOR_WOOD_PARQUET
    },
    "LIVING_DINING": {
        "material_name": "Calacatta Nuvolato Italian Marble",
        "texture_file": "marble_italian.png",
        "fallback_color": FLOOR_MARBLE_ITALIAN
    },
    "CIRCULATION": {
        "material_name": "Calacatta Nuvolato Italian Marble",
        "texture_file": "marble_italian.png",
        "fallback_color": FLOOR_MARBLE_ITALIAN
    },
    "KITCHEN": {
        "material_name": "Verde Sage Honed Quartzite",
        "texture_file": "stone_sage.png",
        "fallback_color": FLOOR_STONE_SAGE
    },
    "BATHROOM": {
        "material_name": "Pietra Grey Charcoal Slate Tile",
        "texture_file": "tile_charcoal.png",
        "fallback_color": FLOOR_TILE_CHARCOAL
    },
    "BALCONY_TERRACE": {
        "material_name": "Flamed Basalt Exterior Paver",
        "texture_file": "paver_exterior.png",
        "fallback_color": FLOOR_PAVER_EXTERIOR
    },
    "DOUBLE_HEIGHT_VOID": {
        "material_name": "Open-to-Below Air Volume",
        "texture_file": None,
        "fallback_color": "#FFFFFF"
    }
}

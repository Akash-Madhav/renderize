# Architectural Rendering Style & Material Specification Guide

This specification defines the exact visual language, material textures, hex colors, line weights, and shadow standards reverse-engineered from professional presentation sheets (including the reference `DIRECTOR SHEET 1.pdf`).

---

## 1. Master Color Palette

### 1.1 Structural & Enclosure Elements
- **Sheet Background**: `#F7FBFE` (Cool architectural off-white; softens contrast compared to harsh `#FFFFFF`).
- **External Load-Bearing Walls**: `#24282B` (Solid rich graphite / charcoal; communicates mass).
- **Internal Partition Walls**: `#3A3E41` (Deep slate charcoal).
- **Structural Column Accents / Caps**: `#B8A040` (Warm gold / amber accent placed at corner column junctions).
- **Wall Drop Shadow**: `#1A1E21` rendered at 25% opacity with an 8px gaussian blur offset ($+6px\ X, +6px\ Y$ representing South-East sun angle).
- **Window Glazing Accent**: `#00B5B8` (Crisp cyan/teal line highlight representing polished glass reflectiveness).
- **Door Leaf & Millwork**: `#6B4226` (Natural rich walnut/teak brown).

### 1.2 Flooring Materials by Room Typology

| Zone / Room Type | Material Name | Base Color | Texture Motif | Reflectivity / Finish |
| :--- | :--- | :--- | :--- | :--- |
| **Bedrooms** | Warm French Oak Parquet | `#8B6914` to `#A0522D` | Herringbone pattern (45° staggered planks) | Satin wood finish, subtle plank bevels |
| **Living / Dining / Foyers** | Calacatta Nuvolato Marble | `#E0E5DF` to `#F7FBFA` | Light grey/greige organic marble veins | Polished large format tiles with hairline grout |
| **Kitchen / Pantry** | Verde Sage Honed Quartzite | `#8B9E7A` to `#B5C4A8` | Fine directional grain stone | Matte honed surface |
| **Main Bathrooms** | Pietra Grey Porcelain | `#3A4550` to `#474B4E` | Charcoal tile grid ($600\times600mm$) | Slip-resistant matte |
| **En-suite / Vanity Bathrooms** | Terrazzo Venato | `#C8B8A8` to `#D4C4B4` | Fine speckled aggregates in warm beige | Polished aggregate |
| **Staircase Treads & Landings** | Cast White Terrazzo | `#F0F2F5` with dark specs | Linear nosing line with stippled landing | Textured concrete / stone |
| **Balconies & Open Terraces** | Flamed Basalt Paver | `#B8BDB5` to `#C8CCC7` | Rectangular paver grid ($300\times600mm$) | Exterior weathered stone |
| **Double Height Void** | Open-to-Below Air Space | `#FFFFFF` with `#888888` dashed line | Diagonal $X$ vector cross-hatch | Negative space |

---

## 2. Furniture & Staging Visualization Standards

Furniture items are rendered in **flat architectural plan-view** (not 3D perspectives) with delicate drop shadows:

1. **Beds**:
   - Timber headboard and base frame in deep walnut (`#4A2E1B`).
   - High-thread-count white/cream duvet with decorative textured throw runner in forest green or slate grey (`#3A4A3E`).
   - Twin bedside nightstands with reading lamp circles.
2. **Sofas & Lounge Chairs**:
   - Modern minimalist silhouette with soft edge radiuses.
   - Upholstery in warm olive drab (`#4A5E3A`) or neutral linen (`#D8D3C8`).
   - Coffee tables in smoked glass or fluted oak.
3. **Dining Ensembles**:
   - Solid walnut/oak dining table top.
   - Minimalist chairs tucked beneath the tabletop edge.
4. **Kitchen Counters & Fixtures**:
   - Double bowl stainless steel sink with swivel faucet circle.
   - Induction 4-burner cooktop plate with subtle ring outlines.
   - Full-depth refrigerator and pantry tall unit blocks.
5. **Sanitary Ware**:
   - Plan-view porcelain white (`#FFFFFF`) with dark charcoal outline (`#24282B` at 0.5pt).

---

## 3. Typography & Annotation Formatting

To preserve presentation legibility:
- **Sheet Title**: Classic Didone/Serif typeface (Playfair Display, Bodoni, Georgia), Uppercase, tracked $+100$.
- **Drawing Titles**: Geometric Sans-Serif (Inter, Helvetica, Arial), Bold, Uppercase, tracked $+50$, accompanied by underline or subtitle.
- **Dimension Text**: Clean compact Sans-Serif, 7pt–8pt at sheet scale, positioned directly along dimension witness lines.
- **Section Cut Markers**: Heavy dashed line (`#404040`, 1.5pt width) terminating in directional filled triangles and letter callouts (e.g., `A — A'`).
- **North Arrow**: Minimalist modern circular badge with shaded northern arrow quadrant.

---

## 4. Resolution & Export Standards

- **Working Resolution**: 300 DPI minimum ($11.81\ \text{pixels/mm}$).
- **Standard A1 Presentation Sheet**: $841\text{mm} \times 594\text{mm}$ $\rightarrow$ $9,933 \times 7,016\ \text{pixels}$.
- **Export Formats**:
  1. Print-Ready Multi-Layer Vector/Raster PDF.
  2. High-Resolution Compressed Presentation PNG.

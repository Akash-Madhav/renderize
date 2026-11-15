# Architectural Quality Assurance Checklist & Validation Protocol

This document outlines the mandatory QA audit protocol that must be completed before delivering any rendered architectural drawings to clients or users.

---

## 1. Automated Geometric Verification Criteria

| Check Code | Verification Item | Metric / Threshold | Failure Action |
| :--- | :--- | :--- | :--- |
| **GEO-01** | Wall Axis Displacement | Max allowable deviation $< 1.5\text{px}$ against vector CAD source | Re-rasterize vector wall mask directly |
| **GEO-02** | Room Perimeter Closure | 100% of rooms must be topologically closed polygons | Re-run morphological closing on partition lines |
| **GEO-03** | Door Opening Retention | $100\%$ door count matching source CAD drawing | Verify door leaf threshold gap closing |
| **GEO-04** | Window Openings | $100\%$ window count matching source CAD drawing | Re-map fenestration along perimeter envelope |
| **GEO-05** | Dimension Text Preservation | 100% numerical values preserved in exact coordinates | Overlay vector annotation layer directly on top |
| **GEO-06** | Scale Integrity | Multi-level plans must match exactly in pixel-per-meter scaling | Enforce common DPI matrix multiplier |

---

## 2. Visual & Architectural Sanity Checklist

### 2.1 Spatial Functionality & Circulation
- [ ] **Egress Clearances**: Corridors maintain clear passage $\ge 1.0m$; no furniture encroaching on circulation paths.
- [ ] **Door Clearances**: All door swing arcs are 100% unobstructed by beds, wardrobes, nightstands, or bathroom fixtures.
- [ ] **Wet Area Placement**: Vanities, water closets, and showers are located exclusively within wet-zoned rooms.
- [ ] **Vertical Continuity**: Stairs and plumbing shafts align directly above/below one another across all levels.
- [ ] **Void Integrity**: Double-height open voids are rendered as open space (diagonal $X$ line) without solid flooring.

### 2.2 Material & Texture Standards
- [ ] **Texture Scale**: Wood plank widths, tile grids, and stone veining match architectural scale ($1:50$ / $1:100$).
- [ ] **Seamless Tiling**: No visible tiling seams, repeating grid lines, or unnatural edge boundaries.
- [ ] **Zone Consistency**: Identical room types across floors (e.g., Master Bedrooms) use harmonious material specifications.
- [ ] **Boundary Masking**: Textures stop cleanly at inner wall faces with zero color bleeding into wall cores.

### 2.3 Lighting, Shading & Graphics
- [ ] **Consistent Sun Angle**: Shadows cast strictly in one unified direction across all floor plans (South-East, $45^\circ$).
- [ ] **Ambient Occlusion**: Soft depth gradient present at wall-floor intersections.
- [ ] **Glazing Accent**: Windows clearly identified with vibrant cyan/teal line highlight (`#00B5B8`).
- [ ] **Structural Highlights**: Gold/amber column caps (`#B8A040`) present at primary grid intersections.

### 2.4 Annotation & Composition
- [ ] **Text Legibility**: Dimension strings, room identifiers, and titles are crisp and legible at $100\%$ zoom.
- [ ] **North Arrow**: Present, orienting correctly according to project site context.
- [ ] **Sheet Balance**: White space is balanced; title blocks and legends align cleanly to page margins.

---

## 3. Difference Overlay Verification Protocol

When validating a rendered drawing against its original CAD PDF:
1. Export the source vector CAD drawing as a pure black-on-white line rendering at $300\ \text{DPI}$.
2. Invert the line rendering so walls and symbols are highlighted in vivid red (`#FF0000`).
3. Set the red line mask to $40\%$ opacity and composite it directly over the rendered presentation output.
4. Visually inspect the composite:
   - **Correct**: All red lines sit exactly centered inside the charcoal wall fills and furniture footprints.
   - **Defect (Shift)**: Any red line peeking outside a rendered wall indicates geometric distortion $\rightarrow$ **Reject & Re-render**.
   - **Defect (Missing)**: Any red line floating over an empty floor texture indicates a missing wall $\rightarrow$ **Reject & Re-render**.

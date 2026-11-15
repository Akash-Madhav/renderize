---
name: architectural-plan-renderer
description: Transforms technical architectural floor plan PDFs (CAD exports) into professionally rendered architectural presentation drawings with realistic materials, textures, furniture visualization, and presentation boards. Use when a user uploads architectural PDF drawings and wants them analyzed or rendered into publication-quality presentation plans while strictly preserving geometric accuracy, wall positions, and dimensions.
---

# Architectural Plan Renderer Skill

An expert AI architectural visualization system designed to read, analyze, interpret, and render architectural technical floor plans (CAD exports, line drawings, PDF blueprints) into publication-grade presentation drawings.

This skill prioritizes **architectural reasoning and structural fidelity over arbitrary visual generation**.

---

## 1. Core Operating Philosophy

1. **Geometry is Invariant**: Never move, hallucinate, erase, or distort walls, columns, door swings, window openings, or room boundaries.
2. **Strict Building Envelope Isolation**: Textures and flooring materials must be strictly confined to the internal built volume and bounded balconies. Zero texture bleed is permitted beyond exterior structural walls into dimension lines, grid markers, or page margins.
3. **Reasoning Precedes Rendering**: Infer room typologies, functional zoning, circulation paths, and structural hierarchy before assigning materials or visual styling.
4. **Decoupled Architecture**: Measurable geometry (vector paths, scale, dimensions) is processed deterministically; styling (textures, lighting, shadows, staging) is applied selectively without compromising the geometric substrate.
5. **Intelligent Architectural Framing**: Crop and present the plan based on the actual building footprint plus its immediate dimension collar, eliminating excessive blank CAD sheet margins.

---

## 2. Multi-Stage Architectural Transformation Workflow

```
[Input Vector/Raster PDF]
       │
       ▼
Phase 1: Drawing Extraction & Comprehension (PyMuPDF / pdfplumber)
       │
       ▼
Phase 2: Architectural Geometric & Topological Analysis (OpenCV / Shapely)
       │
       ▼
Phase 3: Semantic Understanding & Spatial Reasoning (Claude Architectural Logic)
       │
       ▼
Phase 4: Rendering Strategy & Material Specification (Design Palette Mapping)
       │
       ▼
Phase 5: Layer-Based Visual Rendering (Pillow / Shader / Sprites)
       │
       ▼
Phase 6: Presentation Board Composition & PDF Export (PyMuPDF / ReportLab)
       │
       ▼
Phase 7: Architectural Quality Assurance (Deviation & Fidelity Validation)
```

---

## 3. Step-by-Step Execution Protocol

### Phase 1: Drawing Comprehension & Extraction
When a user provides one or more architectural PDF files:
1. **Inspect Document Metadata**:
   - Determine whether the PDF is vector-native (containing lines, rects, curves) or raster-scanned.
   - Extract page dimensions (points, inches, or mm), page count, and embedded scale indicators.
   - Run `python scripts/extract_pdf.py --input <path_to_pdf>` to extract raw primitives and text annotations.
2. **Isolate Text & Dimension Annotations**:
   - Extract dimension values (e.g., `4.89 m`, `5.50 m`) and spatial coordinates.
   - Cache annotations to re-impose cleanly onto final rendered layers.

### Phase 2: Geometric & Topological Analysis
Execute `python scripts/analyze_geometry.py --input <extracted_data.json>` to build the **Architectural Model**:
1. **Wall Network Identification**:
   - Cluster parallel line strokes representing wall thickness.
   - Differentiate external perimeter walls (structural enclosure) from internal partitions.
   - Identify structural column/pillar locations at grid intersections.
2. **Opening & Boundary Closure**:
   - Detect door openings and swing arcs (quarter-circle paths or gaps).
   - Detect window openings (parallel glazing lines along perimeter walls).
3. **Enclosed Room Segmentation**:
   - Generate polygonized floor boundaries for every room using connected component and watershed algorithms.
   - Compute area ($m^2$ or $sq.ft$) and aspect ratios.

### Phase 3: Semantic Understanding & Architectural Reasoning
Claude reviews the extracted room boundaries and fixtures to infer spatial typology:
1. **Sanitary Fixture Mapping**:
   - Toilet bowl, wash basin, shower/tub symbols $\rightarrow$ Bathroom / En-suite / Powder Room.
2. **Kitchen & Wet Zone Mapping**:
   - Countertop layout, sink, hob/burner circles $\rightarrow$ Kitchen / Pantry / Utility.
3. **Circulation & Living Zones**:
   - Staircase tread patterns $\rightarrow$ Vertical Circulation / Core.
   - Large central open spaces $\rightarrow$ Living / Dining / Foyer.
   - Rooms with double/queen bed footprints $\rightarrow$ Master Bedroom / Bedroom / Guest Suite.
   - Diagonal cross-hatch ($X$) within double floor volumes $\rightarrow$ Cut-out Void / Open-to-Below.
4. **Consistency Verification**:
   - Cross-check inferred room counts against building typology (e.g., 4 BHK + Library + Office).

### Phase 4: Rendering Strategy & Material Assignment
Map semantic zones to high-fidelity materials derived from `references/material-palette.md`:
- **Bedrooms**: Warm herringbone wood parquet (`#8B6914` to `#A0522D`).
- **Living, Dining & Hallways**: Veined Italian marble or polished light stone (`#E0E5DF` to `#F7FBFA`).
- **Kitchen**: Honed sage-green stone or polished quartzite (`#8B9E7A` to `#B5C4A8`).
- **Bathrooms**: Wet-rated dark ceramic or matte charcoal slate (`#3A4550`) with terrazzo accents (`#C8B8A8`).
- **Staircase**: Natural stone treads with speckled terrazzo landing.
- **Balconies & Terraces**: Non-slip exterior pavers or wood decking.
- **Walls**: Solid charcoal structural core (`#24282B`) with accent caps at columns (`#B8A040`).
- **Windows**: Glazing tint line in vibrant cyan/teal (`#00B5B8`).

### Phase 5: Layer-Based Visual Rendering & Envelope Boundary Protection
Run `python scripts/render_plan.py`:
1. **Layer 0 (Canvas Background)**: Off-white neutral background (`#F7FBFE`).
2. **Layer 1 (Building Envelope Mask)**: Morphologically extracted perimeter enclosing all habitable rooms and perimeter balconies. Everything outside is strictly protected from texture spills.
3. **Layer 2 (Floor Textures - Zero Bleed)**: Masked polygon fills using seamless tileable textures, strictly intersected with `solid_envelope`.
4. **Layer 3 (Wall Structure)**: Crisp charcoal fills (`#24282B`) applied to structural walls within the envelope.
5. **Layer 4 (Glazing & Millwork)**: Door leaves, swing lines, and window glazing lines.
6. **Layer 5 (Furniture Staging)**: Rendered plan-view furniture sprites positioned at CAD symbol coordinates.
7. **Layer 6 (Drop Shadows & Ambient Occlusion)**: Directional soft shadows cast by exterior walls.
8. **Layer 7 (Dimension Collar & CAD Vector Overlay)**: Sharp black dimension lines, witness tick marks, values (`4.89 m`, `5.50 m`), and section markers preserved on clean off-white background with 100% geometric fidelity.
9. **Layer 8 (Auto-Cropped Framing)**: Automatically frames the drawing extents to the architectural envelope plus dimension collar (10% padding), eliminating dead sheet margins.

### Phase 6: Dynamic N-Floor Presentation Board Composition
When producing final deliverables or multi-level sheets:
- Run `python scripts/compose_sheet.py` supporting arbitrary $N$ floor plans ($1, 2, 3, 4, 5+$ levels).
- **Adaptive Layout Engine**:
  - $1$ Plan: Single large presentation board ($1:50$ scale plan, Section AA', Elevation, Material Palette, and Title Block).
  - $2$ Plans: Dual-register presentation board (Ground + Upper floor, Section, Elevation, Schedules).
  - $3$ Plans: Standard tri-column top register matching the `DIRECTOR SHEET 1.pdf` reference layout.
  - $4+$ Plans: Adaptive multi-row grid ($2 \times 2$ or $2 \times 3$) on A1 sheet with balanced proportions.
- Export high-resolution presentation PDF (A1/A2/A3 standard) and 300+ DPI PNG ($9933 \times 7016\text{px}$).

### Phase 7: Quality Assurance & Validation
Execute `python scripts/validate_output.py`:
- Run automated geometric overlap check between input line vectors and rendered walls.
- Verify 100% retention of dimension labels and door locations.
- Verify zero wall displacement or invented rooms.

---

## 4. Non-Negotiable Architectural Constraints

1. **Zero Hallucination of Walls**: Never add walls where none exist; never remove existing partitions.
2. **Opening Fidelity**: Every door and window must maintain its original CAD position and clear opening width.
3. **Clear Circulation**: Furniture must never obstruct doors, corridors, or fire egress routes.
4. **Dimension Protection**: Never alter numerical values of dimension annotations.
5. **Scale Consistency**: Multi-floor presentation boards must render all floor plans at the identical architectural scale.
6. **Ambiguity Escalation**: If drawing elements are illegible or ambiguous, flag them explicitly for user clarification rather than guessing.

---

## 5. Associated Reference Guides

- `references/architectural-reasoning.md`: In-depth spatial analysis, room classification heuristics, and architectural symbol dictionaries.
- `references/material-palette.md`: Complete color swatches, hex codes, texture tiling rules, and lighting standards.
- `references/pipeline-technical-ref.md`: Technical documentation for Python scripts, APIs, and data structures.
- `references/qa-checklist.md`: Step-by-step quality audit checklist for rendered architectural drawings.
- `references/saas-architecture.md`: Specification for scaling this skill into an automated cloud SaaS platform.

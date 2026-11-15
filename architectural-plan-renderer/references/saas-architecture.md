# SaaS Platform Architecture & Evolution Strategy

This specification details how the **Architectural Plan Renderer** Claude Skill transitions into the core intelligence layer of a scalable, multi-tenant B2B/B2C SaaS platform: **Renderize.ai**.

---

## 1. System Vision & Value Proposition

- **Target Audience**: Architects, interior designers, real estate developers, CAD drafters, real estate marketing agencies.
- **Problem**: Manually rendering black-and-white CAD floor plans in Photoshop or 3ds Max takes 4–8 hours per sheet and costs $150–$400 per plan.
- **Solution**: Instant, AI-driven architectural plan rendering in under 3 minutes with guaranteed geometric accuracy, customizable material palettes, and print-ready multi-page presentation boards.

---

## 2. Multi-Tier Microservices Architecture

```mermaid
flowchart TD
    subgraph Client["Web & API Consumers"]
        WebUI["Next.js Web Application\n(Interactive Canvas + Style Picker)"]
        RevitPlugin["Revit / ArchiCAD Export Add-on"]
        RestAPI["Public REST / GraphQL API"]
    end

    subgraph Gateway["API Gateway & Auth"]
        Ingress["Kong / Cloudflare API Gateway"]
        Auth["Auth0 / Clerk Identity Service"]
        Billing["Stripe Metered Billing Engine"]
    end

    subgraph CoreBackend["Application & Orchestration"]
        AppServer["FastAPI Service Mesh"]
        JobQueue["Celery + Redis / RabbitMQ Queue"]
        DB["PostgreSQL (Projects, Schemas, Palettes)"]
        S3["AWS S3 / Cloudflare R2 (PDFs, Textures, Deliverables)"]
    end

    subgraph Intelligence["GPU Rendering & Analysis Workers"]
        Worker1["Vector CAD Extraction Worker (PyMuPDF)"]
        Worker2["Spatial Topology & Segmentation Worker (OpenCV + Shapely)"]
        Worker3["Claude Agent Reasoning Service (Spatial Inference & Staging)"]
        Worker4["Layered Composite & Texture Shading Engine (Pillow + PyTorch)"]
        Worker5["QA & Geometric Verification Validator"]
    end

    WebUI --> Ingress
    RevitPlugin --> Ingress
    RestAPI --> Ingress

    Ingress --> Auth
    Ingress --> AppServer
    AppServer --> DB
    AppServer --> Billing
    AppServer --> JobQueue

    JobQueue --> Worker1
    Worker1 --> Worker2
    Worker2 --> Worker3
    Worker3 --> Worker4
    Worker4 --> Worker5
    Worker5 --> S3
```

---

## 3. End-to-End User Experience Lifecycle

```mermaid
sequenceDiagram
    autonumber
    actor User as Architect / Client
    participant UI as Next.js Web App
    participant API as FastAPI Backend
    participant Worker as Geometry & AI Worker
    participant S3 as Storage Bucket

    User->>UI: Uploads Vector CAD PDF (e.g. 3-floor plans)
    UI->>API: POST /api/v1/projects/render
    API->>S3: Store raw source PDF
    API->>Worker: Enqueue Extraction & Analysis Job
    Worker->>Worker: PyMuPDF vector parse + OpenCV room segmentation
    Worker->>Worker: Claude reasoning classifies rooms & infers furniture
    Worker-->>UI: Real-time WebSocket: "Rooms Detected: 4 Bed, 4 Bath, Kitchen, Living"
    UI->>User: Displays interactive plan with room labels & material choices
    User->>UI: Customizes style (e.g., "Warm Minimalist Oak", "Teal Glazing")
    User->>UI: Clicks "Generate Presentation Board"
    UI->>API: POST /api/v1/jobs/render/execute
    API->>Worker: Layered rendering + drop shadows + high-res texture tiling
    Worker->>Worker: Automated QA overlay validation (< 1.5px deviation)
    Worker->>S3: Upload 300 DPI A1 Presentation PDF & PNGs
    Worker-->>UI: Job Complete event with download URLs
    UI->>User: Interactive pan/zoom viewer + One-click PDF download
```

---

## 4. Key Platform Features

### 4.1 Interactive Spatial Review & Editor
- Architects can review detected rooms before final rendering.
- Quick override dropdown (e.g., change "Study" to "Bedroom" or switch parquet from "Herringbone" to "Linear Plank").
- Live material palette swap with instant thumbnail preview.

### 4.2 Presentation Board Layout Generator
- Multi-sheet templates (A1, A2, Arch D, 16:9 Landscape) with configurable layouts:
  - 3-Floor Villa Stack (Ground, First, Second + Section AA' + Roof).
  - Apartment Comparison Board (2-BHK vs 3-BHK).
  - Title block customizer with firm logo, project area, scale, and north indicator.

### 4.3 Enterprise API & CAD Integrations
- Direct export from AutoCAD, Revit, and ArchiCAD via desktop plugin.
- Headless API for real estate property listing portals (Zillow, Rightmove, 99acres) to auto-render developer blueprints into attractive listing graphics.

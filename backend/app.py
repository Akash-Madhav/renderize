"""
app.py - Main FastAPI Application Entrypoint
"""

import sys
from pathlib import Path

# Add backend directory to path
backend_path = Path(__file__).resolve().parent
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path.parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.config import ALLOWED_ORIGINS, RENDERS_DIR
from backend.api.routes_projects import router as projects_router
from backend.api.routes_downloads import router as downloads_router

app = FastAPI(
    title="Renderize Architectural Plan Rendering API",
    description="Full-stack AI-assisted architectural floor plan rendering engine.",
    version="1.0.0"
)

# CORS middleware for Next.js frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all during local development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Routers
app.include_router(projects_router)
app.include_router(downloads_router)


@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "renderize-backend",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    from backend.config import HOST, PORT
    print(f"Starting Renderize FastAPI Server on http://{HOST}:{PORT}")
    uvicorn.run("backend.app:app", host=HOST, port=PORT, reload=False)

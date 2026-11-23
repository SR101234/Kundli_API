"""FastAPI main entrypoint with CORS, OpenAPI metadata, and routing."""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from kundli.api.routes.kundli_router import router as kundli_router
from kundli.api.routes.admin_router import router as admin_router

app = FastAPI(
    title="Complete Vedic & KP Kundli Calculation Engine API",
    description="High-precision Vedic Astrology and Krishnamurti Paddhati (KP) Calculation Engine powered by Swiss Ephemeris.",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(kundli_router)
app.include_router(admin_router)


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/api/status")
def api_status():
    return {
        "engine": "Complete Kundli Calculation Engine",
        "version": "1.0.0",
        "docs_url": "/docs",
        "status": "online"
    }


# Mount static React frontend if built
dist_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "frontend", "dist")
if os.path.exists(dist_dir):
    app.mount("/", StaticFiles(directory=dist_dir, html=True), name="static_frontend")
else:
    @app.get("/")
    def root():
        return {
            "engine": "Complete Kundli Calculation Engine",
            "version": "1.0.0",
            "docs_url": "/docs",
            "status": "online"
        }

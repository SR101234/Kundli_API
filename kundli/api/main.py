"""FastAPI main entrypoint with CORS, OpenAPI metadata, production middleware, and static frontend mounting."""
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from kundli.config import CORS_ORIGINS, ENVIRONMENT, MONGO_DB_NAME
from kundli.db.database import get_db, get_client
from kundli.api.routes.kundli_router import router as kundli_router
from kundli.api.routes.admin_router import router as admin_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Graceful startup and shutdown for database connection pool."""
    # Initialize DB connection on startup
    try:
        db = get_db()
        db.command("ping")
    except Exception as e:
        print(f"⚠️ Warning: MongoDB initial ping failed: {e}")
    yield
    # Cleanup on shutdown
    try:
        client = get_client()
        client.close()
    except Exception:
        pass


app = FastAPI(
    title="Complete Vedic & KP Kundli Calculation Engine API",
    description="High-precision Vedic Astrology and Krishnamurti Paddhati (KP) Calculation Engine powered by Swiss Ephemeris and MongoDB.",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs" if ENVIRONMENT != "production_hidden" else None,
    redoc_url="/redoc" if ENVIRONMENT != "production_hidden" else None
)

# 1. GZip Compression Middleware (min 1KB)
app.add_middleware(GZipMiddleware, minimum_size=1000)

# 2. CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS if "*" not in CORS_ORIGINS else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Production Security Headers Middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response


# Include Subsystem Routers
app.include_router(kundli_router)
app.include_router(admin_router)


@app.get("/health", summary="Production Health & MongoDB Status")
def health():
    """Health check endpoint verifying process uptime and MongoDB connectivity."""
    db_status = "connected"
    try:
        db = get_db()
        db.command("ping")
    except Exception as err:
        db_status = f"degraded: {str(err)}"

    is_healthy = "degraded" not in db_status
    status_code = 200 if is_healthy else 503
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "healthy" if is_healthy else "degraded",
            "database": "mongodb",
            "db_name": MONGO_DB_NAME,
            "db_status": db_status,
            "environment": ENVIRONMENT
        }
    )


@app.get("/api/status", summary="Engine Status & Metadata")
def api_status():
    return {
        "engine": "Complete Vedic & KP Kundli Engine",
        "version": "1.0.0",
        "database": "mongodb",
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
            "engine": "Complete Vedic & KP Kundli Engine",
            "version": "1.0.0",
            "database": "mongodb",
            "docs_url": "/docs",
            "status": "online",
            "frontend": "Frontend dist not found. Please build frontend/dist."
        }

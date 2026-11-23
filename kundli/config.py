"""Production configuration loader for Kundli Engine."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env file if present
load_dotenv(BASE_DIR / ".env")

# Database (MongoDB)
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "kundli_db")

# Admin Security
ADMIN_KEY = os.getenv("ADMIN_KEY", "admin@kundli2026")
DEFAULT_CHECK_LIMIT = int(os.getenv("DEFAULT_CHECK_LIMIT", "10"))

# Server & Environment
ENVIRONMENT = os.getenv("ENVIRONMENT", "production")
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
WORKERS = int(os.getenv("WORKERS", "2"))

# CORS settings (comma-separated origins or * for all)
_cors_raw = os.getenv("CORS_ORIGINS", "*")
CORS_ORIGINS = [orig.strip() for orig in _cors_raw.split(",") if orig.strip()]

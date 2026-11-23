"""Server startup script for Kundli Backend & Frontend."""
import os
import sys
import uvicorn
from kundli.config import HOST, PORT, WORKERS, ENVIRONMENT

if __name__ == "__main__":
    # Ensure current directory is on pythonpath
    sys.path.insert(0, os.path.dirname(__file__))
    print(f"✨ Starting Vedic & KP Kundli Engine in [{ENVIRONMENT}] mode")
    print(f"🌐 Server URL: http://{HOST if HOST != '0.0.0.0' else '127.0.0.1'}:{PORT}")
    print(f"📖 OpenAPI / Swagger Docs: http://{HOST if HOST != '0.0.0.0' else '127.0.0.1'}:{PORT}/docs")
    
    is_dev = ENVIRONMENT.lower() in ("development", "dev")
    uvicorn.run(
        "kundli.api.main:app",
        host=HOST,
        port=PORT,
        workers=1 if is_dev else WORKERS,
        reload=is_dev
    )

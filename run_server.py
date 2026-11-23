"""Server startup script for Kundli Backend & Frontend."""
import uvicorn
import sys
import os

if __name__ == "__main__":
    # Ensure current directory is on pythonpath
    sys.path.insert(0, os.path.dirname(__file__))
    print("✨ Starting Complete Vedic & KP Kundli Engine on http://127.0.0.1:8000")
    print("📖 OpenAPI / Swagger Docs: http://127.0.0.1:8000/docs")
    uvicorn.run("kundli.api.main:app", host="127.0.0.1", port=8000, reload=True)

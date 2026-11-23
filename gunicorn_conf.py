"""Gunicorn production configuration for Hostinger VPS KVM 2."""
import os
import multiprocessing

# Server socket
bind = f"{os.getenv('HOST', '0.0.0.0')}:{os.getenv('PORT', '8001')}"

# Worker processes (Hostinger KVM 2 has 2 vCPUs; 2-4 workers is optimal)
workers = int(os.getenv("WORKERS", "2"))
worker_class = "uvicorn.workers.UvicornWorker"

# Worker lifecycle
timeout = 120
keepalive = 65
max_requests = 2000
max_requests_jitter = 200

# Logging
accesslog = "-"
errorlog = "-"
loglevel = os.getenv("LOG_LEVEL", "info")

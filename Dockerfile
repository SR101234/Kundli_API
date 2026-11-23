# ==============================================================================
# Multi-stage Production Dockerfile for Complete Vedic & KP Kundli Engine
# Optimized for Hostinger VPS KVM 2 (2 vCPUs, 8 GB RAM)
# ==============================================================================

FROM python:3.12-slim AS builder

WORKDIR /app

# Install OS build dependencies for compiling pyswisseph C bindings
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    python3-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python requirements into virtual env
COPY requirements.txt .
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip wheel && \
    pip install --no-cache-dir -r requirements.txt

# ==============================================================================
# Runner Image (Lean & Secure)
# ==============================================================================
FROM python:3.12-slim AS runner

WORKDIR /app

# Install runtime libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy virtualenv from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Copy application source code and pre-compiled frontend distribution
COPY kundli/ kundli/
COPY frontend/dist/ frontend/dist/
COPY gunicorn_conf.py .
COPY run_server.py .

# Create non-root user for security
RUN useradd -u 1001 -m kundliuser && \
    chown -R kundliuser:kundliuser /app
USER kundliuser

EXPOSE 8000

# Healthcheck probe
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Production command: Gunicorn with Uvicorn workers
CMD ["gunicorn", "-c", "gunicorn_conf.py", "kundli.api.main:app"]

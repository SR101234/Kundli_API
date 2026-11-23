#!/usr/bin/env bash
# ==============================================================================
# One-Click Deployment Script for Prod_Kundli (MERN + Swiss Ephemeris)
# Optimized for Hostinger VPS KVM 2 with PM2 & Nginx
# ==============================================================================

set -euo pipefail

GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${CYAN}================================================================${NC}"
echo -e "${CYAN}   🚀 Deploying Prod_Kundli (MERN Engine) with PM2 & Nginx     ${NC}"
echo -e "${CYAN}================================================================${NC}"

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

# 1. Create logs directory
mkdir -p "$DIR/logs"

# 2. Environment Configuration
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚙️ Creating .env configuration from .env.example...${NC}"
    cp .env.example .env
fi

# 3. Setup Python virtual environment for Swiss Ephemeris calculations
VENV_DIR="$DIR/.venv"
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}🐍 Setting up Python virtual environment for Swiss Ephemeris...${NC}"
    python3 -m venv "$VENV_DIR"
fi

echo -e "${YELLOW}📦 Installing / verifying Python calculation dependencies...${NC}"
"$VENV_DIR/bin/pip" install --upgrade pip wheel
"$VENV_DIR/bin/pip" install -r requirements.txt

# 4. Install Node.js Dependencies
echo -e "${YELLOW}📦 Installing Node.js Express dependencies...${NC}"
npm install --omit=dev

# 5. Check MongoDB status
echo -e "${YELLOW}🍃 Checking MongoDB status...${NC}"
if systemctl is-active --quiet mongod; then
    echo -e "${GREEN}✅ Local MongoDB service is running.${NC}"
elif command -v docker &> /dev/null && docker ps | grep -q "kundli-mongo"; then
    echo -e "${GREEN}✅ Docker MongoDB container is running.${NC}"
elif command -v docker &> /dev/null; then
    echo -e "${YELLOW}🐳 Starting MongoDB in Docker container on 127.0.0.1:27017...${NC}"
    docker run -d --name kundli-mongo -p 27017:27017 -v mongo_data:/data/db --restart unless-stopped mongo:7.0 || true
else
    echo -e "${YELLOW}⚠️ Ensure MongoDB is accessible at mongodb://127.0.0.1:27017/kundli_db.${NC}"
fi

# 6. Verify / Install PM2
if ! command -v pm2 &> /dev/null; then
    echo -e "${YELLOW}📦 Installing PM2 globally...${NC}"
    npm install -g pm2
fi

# 7. Release port 8005 if occupied by earlier containers or processes
echo -e "${YELLOW}🔍 Ensuring port 8005 is free...${NC}"
if command -v fuser &> /dev/null; then
    fuser -k 8005/tcp 2>/dev/null || true
fi

# 8. Start / Restart PM2 Application
echo -e "${YELLOW}⚡ Starting / Reloading application in PM2...${NC}"
pm2 delete prod-kundli-mern 2>/dev/null || true
pm2 start ecosystem.config.js
pm2 save

# 9. Configure Nginx
if [ -d /etc/nginx/conf.d ]; then
    echo -e "${YELLOW}🌐 Updating Nginx configuration in /etc/nginx/conf.d/kundli.conf...${NC}"
    cp "$DIR/nginx.conf" /etc/nginx/conf.d/kundli.conf
    rm -f /etc/nginx/sites-enabled/default.conf || true
    rm -f /etc/nginx/sites-enabled/kundli || true
    if nginx -t; then
        systemctl reload nginx
        echo -e "${GREEN}✅ Nginx reloaded successfully.${NC}"
    else
        echo -e "${RED}⚠️ Nginx configuration test failed. Check /etc/nginx/conf.d/kundli.conf.${NC}"
    fi
fi

# 10. Health Check
echo -e "${YELLOW}⏳ Probing health check at http://127.0.0.1:8005/health...${NC}"
sleep 2
curl -s http://127.0.0.1:8005/health || true

echo -e "\n${GREEN}================================================================${NC}"
echo -e "${GREEN}   ✨ PROD_KUNDLI DEPLOYMENT COMPLETED!                         ${NC}"
echo -e "${GREEN}================================================================${NC}"
echo -e "🌐 Live Domain:         ${CYAN}https://kundli-api.bhagyanetram.com${NC}"
echo -e "🔌 Direct Internal Port:${CYAN}http://127.0.0.1:8005${NC}"
echo -e "❤️ Health Status:       ${CYAN}https://kundli-api.bhagyanetram.com/health${NC}"
echo -e "⚡ PM2 Process Name:    ${YELLOW}prod-kundli-mern${NC}"
echo -e "${GREEN}================================================================${NC}\n"

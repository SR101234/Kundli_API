#!/usr/bin/env bash
# ==============================================================================
# PM2 Setup & Deployment Script for Hostinger VPS KVM 2
# Complete Vedic & KP Kundli Engine (/var/www/Kundli_API)
# ==============================================================================

set -euo pipefail

GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${CYAN}================================================================${NC}"
echo -e "${CYAN}   🚀 Configuring Kundli Engine with PM2 on Hostinger VPS       ${NC}"
echo -e "${CYAN}================================================================${NC}"

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$APP_DIR"

# 1. Create logs directory for PM2
mkdir -p "$APP_DIR/logs"

# 2. Check and setup Python 3 virtual environment
if [ ! -d "$APP_DIR/.venv" ]; then
    echo -e "${YELLOW}🐍 Setting up Python 3 virtual environment...${NC}"
    apt-get update -y
    apt-get install -y python3-venv python3-pip python3-dev build-essential gcc
    python3 -m venv "$APP_DIR/.venv"
fi

echo -e "${YELLOW}📦 Installing / verifying Python dependencies...${NC}"
"$APP_DIR/.venv/bin/pip" install --upgrade pip wheel
"$APP_DIR/.venv/bin/pip" install -r "$APP_DIR/requirements.txt"

# 3. Verify MongoDB is running (either native service or docker container)
echo -e "${YELLOW}🍃 Checking MongoDB connection...${NC}"
if systemctl is-active --quiet mongod; then
    echo -e "${GREEN}✅ Native mongod service is active.${NC}"
elif command -v docker &> /dev/null && docker ps | grep -q "kundli-mongo"; then
    echo -e "${GREEN}✅ Docker MongoDB container is active.${NC}"
elif command -v docker &> /dev/null; then
    echo -e "${YELLOW}🐳 Starting MongoDB in lightweight Docker container on port 27017...${NC}"
    docker run -d --name kundli-mongo -p 27017:27017 -v mongo_data:/data/db --restart unless-stopped mongo:7.0 || true
    echo -e "${GREEN}✅ MongoDB started via Docker on port 27017.${NC}"
else
    echo -e "${YELLOW}⚠️ Notice: Ensure MongoDB is running locally on 127.0.0.1:27017.${NC}"
fi

# 4. Verify PM2 is installed
if ! command -v pm2 &> /dev/null; then
    echo -e "${YELLOW}📦 Installing PM2 globally via npm...${NC}"
    npm install -g pm2
fi

# 5. Start or reload PM2 application
echo -e "${YELLOW}⚡ Starting / Reloading application in PM2...${NC}"
pm2 delete kundli-api 2>/dev/null || true
pm2 start ecosystem.config.js
pm2 save

echo -e "\n${GREEN}================================================================${NC}"
echo -e "${GREEN}   ✨ PM2 PROCESS RUNNING SUCCESSFULLY!                         ${NC}"
echo -e "${GREEN}================================================================${NC}"
pm2 status

echo -e "\n${CYAN}Useful PM2 Commands:${NC}"
echo -e "  - View live logs:     ${YELLOW}pm2 logs kundli-api${NC}"
echo -e "  - Restart backend:    ${YELLOW}pm2 restart kundli-api${NC}"
echo -e "  - Monitor resources:  ${YELLOW}pm2 monit${NC}"
echo -e "  - Process status:     ${YELLOW}pm2 status${NC}\n"

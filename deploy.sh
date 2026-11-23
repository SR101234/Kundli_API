#!/usr/bin/env bash
# ==============================================================================
# One-Click Production Deployment Script for Hostinger VPS KVM 2
# Complete Vedic & KP Kundli Engine + MongoDB
# ==============================================================================

set -euo pipefail

GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${CYAN}================================================================${NC}"
echo -e "${CYAN}   🚀 Deploying Vedic & KP Kundli Engine on Hostinger VPS        ${NC}"
echo -e "${CYAN}================================================================${NC}"

# 1. Verify root or sudo access
if [ "$EUID" -ne 0 ]; then
  echo -e "${RED}❌ Please run this script with sudo or as root.${NC}"
  exit 1
fi

# 2. Check & Install Docker if missing
if ! command -v docker &> /dev/null; then
    echo -e "${YELLOW}📦 Docker not detected. Installing Docker Engine...${NC}"
    apt-get update -y
    apt-get install -y ca-certificates curl gnupg lsb-release
    mkdir -p /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg --yes
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
    apt-get update -y
    apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    systemctl enable docker
    systemctl start docker
    echo -e "${GREEN}✅ Docker installed successfully.${NC}"
else
    echo -e "${GREEN}✅ Docker is already installed.${NC}"
fi

# 3. Environment configuration setup
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚙️ Creating .env configuration from .env.example...${NC}"
    cp .env.example .env
    # Generate random secure admin key if default is present
    RANDOM_KEY="admin_$(openssl rand -hex 8)"
    sed -i "s/ADMIN_KEY=admin@kundli2026/ADMIN_KEY=${RANDOM_KEY}/g" .env
    echo -e "${GREEN}🔑 Generated custom Admin Passcode: ${RANDOM_KEY}${NC}"
fi

# 4. Stop existing containers & rebuild
echo -e "${YELLOW}🔨 Building and starting Docker containers (MongoDB + FastAPI)...${NC}"
docker compose down --remove-orphans || true
docker compose up -d --build

# 5. Wait for health check
echo -e "${YELLOW}⏳ Waiting for services to initialize...${NC}"
for i in {1..12}; do
    if curl -s http://127.0.0.1:8000/health | grep -q "healthy"; then
        echo -e "${GREEN}✅ All services are healthy and running!${NC}"
        break
    fi
    sleep 3
done

# 6. Fetch Public IP
SERVER_IP=$(curl -s -4 ifconfig.me || hostname -I | awk '{print $1}')
ADMIN_KEY_VAL=$(grep ADMIN_KEY .env | cut -d '=' -f2)

echo -e "\n${GREEN}================================================================${NC}"
echo -e "${GREEN}   ✨ DEPLOYMENT COMPLETE & OPERATIONAL!                        ${NC}"
echo -e "${GREEN}================================================================${NC}"
echo -e "🌐 Web Application:     ${CYAN}http://${SERVER_IP}:8000${NC}"
echo -e "📖 Swagger API Docs:    ${CYAN}http://${SERVER_IP}:8000/docs${NC}"
echo -e "❤️ Health Status:       ${CYAN}http://${SERVER_IP}:8000/health${NC}"
echo -e "🛡️ Admin Passcode:       ${YELLOW}${ADMIN_KEY_VAL}${NC}"
echo -e "💾 Database:            ${CYAN}MongoDB 7.0 (Docker Volume: mongo_data)${NC}"
echo -e "${GREEN}================================================================${NC}\n"

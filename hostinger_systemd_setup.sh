#!/usr/bin/env bash
# ==============================================================================
# Bare-Metal Systemd + Native MongoDB Setup for Hostinger VPS KVM 2
# (Alternative to Docker Compose)
# ==============================================================================

set -euo pipefail

if [ "$EUID" -ne 0 ]; then
  echo "Please run as root or sudo"
  exit 1
fi

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
USER_NAME="kundli"

echo "1. Installing system build dependencies and Python 3..."
apt-get update -y
apt-get install -y build-essential python3 python3-pip python3-venv curl gnupg

echo "2. Installing MongoDB Community Edition..."
if ! command -v mongod &> /dev/null; then
    curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | \
       gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg --dearmor --yes
    echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | \
       tee /etc/apt/sources.list.d/mongodb-org-7.0.list
    apt-get update -y
    apt-get install -y mongodb-org
    systemctl enable mongod
    systemctl start mongod
fi

echo "3. Creating dedicated service user..."
id -u $USER_NAME &>/dev/null || useradd -r -s /bin/false $USER_NAME

echo "4. Setting up Python virtual environment..."
python3 -m venv "$APP_DIR/.venv"
"$APP_DIR/.venv/bin/pip" install --upgrade pip wheel
"$APP_DIR/.venv/bin/pip" install -r "$APP_DIR/requirements.txt"

chown -R $USER_NAME:$USER_NAME "$APP_DIR"

echo "5. Installing Systemd service..."
cat << EOF > /etc/systemd/system/kundli.service
[Unit]
Description=Complete Vedic & KP Kundli Engine
After=network.target mongod.service
Wants=mongod.service

[Service]
Type=simple
User=$USER_NAME
Group=$USER_NAME
WorkingDirectory=$APP_DIR
Environment="PATH=$APP_DIR/.venv/bin"
EnvironmentFile=-$APP_DIR/.env
ExecStart=$APP_DIR/.venv/bin/gunicorn -c $APP_DIR/gunicorn_conf.py kundli.api.main:app
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable kundli
systemctl restart kundli

echo "✅ Kundli service installed and started via systemd!"
echo "Check status: systemctl status kundli"

# ☸️ Prod_Kundli: Enterprise MERN + Python Kundli Engine

A production-grade **MERN (MongoDB, Express.js, React, Node.js)** Vedic Astrology and Krishnamurti Paddhati (KP) Calculation Engine integrated with **Swiss Ephemeris (Python)**.

Designed for high-throughput production deployment on **Hostinger VPS KVM 2** with **PM2 Process Manager**, **MongoDB 7.0**, and **Nginx Reverse Proxy with SSL (`kundli-api.bhagyanetram.com`)**.

---

## 🏛️ Architecture Breakdown

```
Browser / Client (https://kundli-api.bhagyanetram.com)
                          │
                          ▼ (Port 443 HTTPS / SSL)
                    Nginx Reverse Proxy
                          │
                          ▼ (Port 8001)
               PM2 Cluster (Node.js Express)
               ├── MongoDB / Mongoose (User Quotas, Lead Contact Logs)
               ├── Static React Frontend (Single Page Application)
               └── Python Calculation Bridge
                          │
                          ▼ (IPC / Stdin-Stdout JSON Stream)
                Swiss Ephemeris Python Engine
                ├── 16 Shodashavargas (D1–D60)
                ├── KP 249 Sub-Lords & Ruling Planets
                ├── Ashtakavarga 337-Point Matrix
                ├── 5-Level Vimshottari & Yogini Dasha
                ├── 36-Gun Milan Marriage Matching
                └── Yogas, Doshas, Shadbala & Transits
```

---

## 🚀 1-Click Deployment on Hostinger VPS

Run on your VPS terminal:
```bash
cd /var/www/Kundli_API/Prod_Kundli
chmod +x deploy_mern.sh
./deploy_mern.sh
```

---

## ⚡ Manual Step-by-Step Setup

### 1. Install Node.js Dependencies
```bash
cd Prod_Kundli
npm install --omit=dev
```

### 2. Setup Python Virtual Environment for Swiss Ephemeris
```bash
python3 -m venv .venv
.venv/bin/pip install --upgrade pip wheel
.venv/bin/pip install -r requirements.txt
```

### 3. Start with PM2
```bash
pm2 start ecosystem.config.js
pm2 save
```

### 4. Configure Nginx
```bash
cp nginx.conf /etc/nginx/conf.d/kundli.conf
nginx -t && systemctl reload nginx
```

---

## 🛡️ Admin Dashboard & 10-Check Quota

- **URL**: `https://kundli-api.bhagyanetram.com` (Click **"🛡️ Admin Panel"** in header).
- **Default Passcode**: Stored in `.env` (`ADMIN_KEY`).
- **Features**:
  - Live KPI stats (total users, generated kundlis, daily activity).
  - Search by name, email, or mobile.
  - 1-click quota resets and custom limit expansions.
  - CSV export of leads with exact birth parameters and timestamps.

---

## 🛠️ Useful PM2 Commands

```bash
# View live application logs
pm2 logs prod-kundli-mern

# Restart cluster with zero downtime
pm2 reload prod-kundli-mern

# Monitor CPU & memory
pm2 monit

# Stop process
pm2 stop prod-kundli-mern
```

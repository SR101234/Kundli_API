# 🚀 Production Deployment Guide: Hostinger VPS KVM 2

Complete guide for deploying the **Vedic & KP Kundli Calculation Engine with MongoDB** on a **Hostinger VPS (KVM 2 plan: 2 vCPUs, 8 GB RAM, 100 GB NVMe)**.

---

## 📋 System Prerequisites

| Item | Details |
| :--- | :--- |
| **Server** | Hostinger VPS KVM 2 |
| **Operating System** | Ubuntu 22.04 LTS or 24.04 LTS (recommended) |
| **Specs** | 2 vCPUs, 8 GB RAM, 100 GB NVMe |
| **Database** | MongoDB 7.0 (Automated in container with persistent volume) |
| **Calculation Engine** | Python 3.12 + Swiss Ephemeris (`pyswisseph`) |
| **Web Server** | FastAPI + Gunicorn (2 Uvicorn workers) |
| **Frontend** | Pre-compiled React + Vite + Tailwind CSS bundle |

---

## ⚡ Method 1: Automated 1-Click Docker Deployment (Recommended)

Docker Compose encapsulates the FastAPI engine, Swiss Ephemeris C libraries, and MongoDB into production-ready containers with automated health checks and auto-restart.

### Step 1: Connect to your Hostinger VPS via SSH
Open your terminal or PowerShell and connect to your VPS:
```bash
ssh root@YOUR_SERVER_IP
```

### Step 2: Upload or Clone the Repository
```bash
cd /opt
# If cloning from GitHub:
git clone https://github.com/YOUR_USERNAME/Kundli-API.git
cd Kundli-API

# OR if uploading via SCP / SFTP from your local machine:
# scp -r Kundli-API root@YOUR_SERVER_IP:/opt/
```

### Step 3: Run the Automated Deployment Script
```bash
chmod +x deploy.sh
./deploy.sh
```

**What `deploy.sh` does automatically:**
1. Installs Docker and Docker Compose plugin if not already present.
2. Creates your `.env` configuration file and generates a secure random `ADMIN_KEY`.
3. Builds the optimized Python 3.12 container with compiled Swiss Ephemeris C bindings.
4. Boots MongoDB 7.0 and creates persistent volume `mongo_data`.
5. Waits for health checks to pass.
6. Displays your live public URLs, Swagger documentation link, and Admin Passcode.

---

## 🛠️ Method 2: Manual Docker Compose Deployment

If you prefer to configure manually:

### 1. Copy Environment File
```bash
cp .env.example .env
nano .env
```
*(Customize `ADMIN_KEY`, `MONGO_DB_NAME`, and `PORT` if desired).*

### 2. Build & Launch Containers
```bash
docker compose up -d --build
```

### 3. Check Container Health
```bash
docker compose ps
curl -i http://localhost:8000/health
```

Output:
```json
{
  "status": "healthy",
  "database": "mongodb",
  "db_name": "kundli_db",
  "db_status": "connected",
  "environment": "production"
}
```

---

## 🌐 Configuring Domain Name & Free HTTPS (SSL) with Nginx

To expose the application on ports 80/443 with your custom domain (e.g. `kundli.yourdomain.com`):

### 1. Point DNS to VPS
In your Hostinger DNS Zone or Cloudflare:
- **Type**: `A`
- **Name**: `@` (or `kundli`)
- **Points to**: `YOUR_SERVER_IP`
- **TTL**: Auto / 300s

### 2. Install Nginx & Certbot on Hostinger VPS
```bash
apt-get update
apt-get install -y nginx certbot python3-certbot-nginx
```

### 3. Apply Nginx Configuration
```bash
cp /opt/Kundli-API/nginx.conf /etc/nginx/sites-available/kundli

# Edit the domain name:
sed -i 's/server_name _;/server_name kundli.yourdomain.com;/' /etc/nginx/sites-available/kundli

# Enable the site:
ln -s /etc/nginx/sites-available/kundli /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl reload nginx
```

### 4. Issue Free SSL Certificate (HTTPS)
```bash
certbot --nginx -d kundli.yourdomain.com --non-interactive --agree-tos -m your-email@example.com
```

Now your Kundli Engine is accessible at **`https://kundli.yourdomain.com`** with automated HTTP-to-HTTPS redirect and SSL renewal!

---

## 🛡️ Admin Panel & Quota Management

- Access the Admin Panel at `https://kundli.yourdomain.com` by clicking the **"🛡️ Admin Panel"** button in the top navigation bar.
- Enter your `ADMIN_KEY` (found in your `.env` file).
- From the Admin Dashboard, you can:
  1. Monitor real-time user registrations and Kundli generations.
  2. Search user contact info (*name, email, mobile*) and exact birth parameters (*latitude, longitude, nakshatra, ascendant*).
  3. Reset any user's 10-check quota in 1 click or grant higher limits.
  4. Export all user lead contacts and birth records to CSV.

---

## 💾 MongoDB Maintenance & Backups

MongoDB stores all data in the persistent Docker volume `mongo_data` at `/var/lib/docker/volumes/Kundli-API_mongo_data/_data`.

### Backup Database:
```bash
docker exec -t kundli-mongo mongodump --db kundli_db --archive=/data/db/kundli_backup_$(date +%F).archive
```

### Restore Database:
```bash
docker exec -i kundli-mongo mongorestore --archive=/data/db/kundli_backup_YYYY-MM-DD.archive
```

### View Live Logs:
```bash
# View app logs:
docker compose logs -f app

# View database logs:
docker compose logs -f mongo
```

### Restart Services:
```bash
docker compose restart
```

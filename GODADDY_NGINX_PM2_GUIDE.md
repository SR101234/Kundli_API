# 🌐 Complete Deployment Guide: PM2 + Nginx + GoDaddy Domain

Step-by-step instructions for running the **Vedic & KP Kundli Engine** using **PM2** on your **Hostinger VPS (`187.126.112.136`)** and exposing it securely via **Nginx** with your **GoDaddy domain**.

---

## 📑 Overview of Architecture

```
User Browser (https://yourdomain.com)
       │
       ▼ (Port 80 / 443 with SSL)
  GoDaddy DNS ──► Hostinger VPS IP (187.126.112.136)
                         │
                         ▼
                    Nginx Reverse Proxy
                         │
                         ▼ (Port 8001)
              PM2 (Process: kundli-api)
              Python FastAPI + Swiss Ephemeris
                         │
                         ▼ (Port 27017)
                     MongoDB 7.0
```

---

## 🛠️ Step 1: Configure GoDaddy DNS

1. Log into your **GoDaddy Account** and open **Domain Portfolio**.
2. Click on your domain name and select **Manage DNS** (or **DNS Records**).
3. Add or update the following records:

| Type | Name | Value (Points to) | TTL | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **A** | `@` | `187.126.112.136` | `1/2 Hour` | Points your root domain (`yourdomain.com`) to your Hostinger VPS. |
| **CNAME** | `www` | `@` | `1/2 Hour` | Points `www.yourdomain.com` to your root domain. |

> **Note for Subdomain (e.g. `kundli.yourdomain.com`)**:
> If you are using a subdomain instead, add an **A** record with Name: `kundli` and Value: `187.126.112.136`.

---

## ⚡ Step 2: Start Backend with PM2 on VPS

Connect to your VPS:
```bash
ssh root@187.126.112.136
cd /var/www/Kundli_API
```

### Run the automated PM2 setup script:
```bash
chmod +x pm2_setup.sh
./pm2_setup.sh
```

Or execute manually if preferred:
```bash
# 1. Install dependencies in virtual environment:
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

# 2. Start with PM2:
pm2 start ecosystem.config.js
pm2 save

# 3. Check status:
pm2 status
```

You will see `kundli-api` listed with status `online` on port `8001`!

---

## 🚀 Step 3: Configure Nginx Reverse Proxy

1. Copy the Nginx configuration template:
```bash
cp /var/www/Kundli_API/nginx.conf /etc/nginx/sites-available/kundli
```

2. Open the file to add your domain:
```bash
nano /etc/nginx/sites-available/kundli
```
Find the line:
```nginx
server_name _;
```
Replace it with your actual GoDaddy domain:
```nginx
server_name yourdomain.com www.yourdomain.com;
```
*(Save and exit with `Ctrl + O`, `Enter`, `Ctrl + X`).*

3. Enable the site and test Nginx:
```bash
ln -sf /etc/nginx/sites-available/kundli /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl reload nginx
```

---

## 🔒 Step 4: Install Free SSL (HTTPS) with Certbot

To enable HTTPS with automatic renewals:

```bash
apt-get update
apt-get install -y certbot python3-certbot-nginx

# Obtain and install SSL certificate:
certbot --nginx -d yourdomain.com -d www.yourdomain.com
```
Follow the prompts (enter your email, agree to terms). Certbot will automatically update Nginx to redirect all HTTP traffic to secure HTTPS!

---

## 🔍 Useful PM2 Management Commands

| Action | Command |
| :--- | :--- |
| **View Live Output Logs** | `pm2 logs kundli-api` |
| **Restart Backend Engine** | `pm2 restart kundli-api` |
| **Stop Backend** | `pm2 stop kundli-api` |
| **Monitor CPU & Memory** | `pm2 monit` |
| **View Process List** | `pm2 list` |
| **Save Process List on Reboot** | `pm2 save` |

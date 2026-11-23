/**
 * PM2 Ecosystem Configuration for Vedic & KP Kundli Engine
 * Optimized for Hostinger VPS KVM 2 (/var/www/Kundli_API)
 */
module.exports = {
  apps: [
    {
      name: "kundli-api",
      script: "run_server.py",
      interpreter: "./.venv/bin/python",
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: "1G",
      env: {
        HOST: "127.0.0.1",
        PORT: 8001,
        ENVIRONMENT: "production",
        MONGO_URI: "mongodb://127.0.0.1:27017",
        MONGO_DB_NAME: "kundli_db",
        DEFAULT_CHECK_LIMIT: 10
      },
      log_date_format: "YYYY-MM-DD HH:mm:ss Z",
      error_file: "./logs/pm2-error.log",
      out_file: "./logs/pm2-out.log",
      merge_logs: true
    }
  ]
};

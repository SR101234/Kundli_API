/**
 * PM2 Ecosystem Configuration for Prod_Kundli MERN Engine
 * Optimized for Hostinger VPS KVM 2 (2 vCPUs, 8 GB RAM)
 */
module.exports = {
  apps: [
    {
      name: "prod-kundli-mern",
      script: "./server/server.js",
      instances: 1,
      exec_mode: "fork",
      autorestart: true,
      watch: false,
      max_memory_restart: "1G",
      env: {
        NODE_ENV: "production",
        PORT: 8005,
        MONGO_URI: "mongodb://127.0.0.1:27017/kundli_db",
        DEFAULT_CHECK_LIMIT: 10
      },
      log_date_format: "YYYY-MM-DD HH:mm:ss Z",
      error_file: "./logs/pm2-error.log",
      out_file: "./logs/pm2-out.log",
      merge_logs: true
    }
  ]
};

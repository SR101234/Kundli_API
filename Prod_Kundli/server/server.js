const path = require('path');
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const compression = require('compression');
const morgan = require('morgan');
const mongoose = require('mongoose');
const dotenv = require('dotenv');

// Load environment variables
dotenv.config({ path: path.resolve(__dirname, '../.env') });
dotenv.config(); // fallback

const connectDB = require('./config/db');
const kundliRoutes = require('./routes/kundliRoutes');
const adminRoutes = require('./routes/adminRoutes');

const app = express();
const PORT = process.env.PORT || 8001;
const HOST = process.env.HOST || '0.0.0.0';

// Connect to MongoDB
connectDB();

// Production Middleware
app.use(cors());
app.use(
  helmet({
    contentSecurityPolicy: false // Allows dynamic SVG and charts rendering
  })
);
app.use(compression());
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

if (process.env.NODE_ENV !== 'test') {
  app.use(morgan('combined'));
}

// Health Check Endpoint
app.get('/health', (req, res) => {
  const isDbConnected = mongoose.connection.readyState === 1;
  return res.status(isDbConnected ? 200 : 503).json({
    status: isDbConnected ? 'healthy' : 'degraded',
    server: 'Express (MERN)',
    database: 'MongoDB',
    db_status: isDbConnected ? 'connected' : 'disconnected',
    timestamp: new Date().toISOString()
  });
});

app.get('/api/status', (req, res) => {
  return res.json({
    engine: 'Prod_Kundli MERN Engine',
    version: '1.0.0',
    runtime: 'Node.js Express + Swiss Ephemeris Python',
    status: 'online'
  });
});

// API Routes
app.use('/api/kundli', kundliRoutes);
app.use('/api/admin', adminRoutes);

// Static frontend serving
const clientDistPath = path.resolve(__dirname, '../client/dist');
app.use(express.static(clientDistPath));

// Catch-all route to serve React Single Page Application (SPA)
app.get('*', (req, res) => {
  res.sendFile(path.join(clientDistPath, 'index.html'));
});

// Start Server
if (process.env.NODE_ENV !== 'test') {
  app.listen(PORT, HOST, () => {
    console.log(`================================================================`);
    console.log(`✨ Prod_Kundli MERN Engine running at http://${HOST}:${PORT}`);
    console.log(`❤️ Health endpoint: http://${HOST}:${PORT}/health`);
    console.log(`================================================================`);
  });
}

module.exports = app;

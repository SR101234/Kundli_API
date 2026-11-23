const express = require('express');
const router = express.Router();
const User = require('../models/User');
const KundliRecord = require('../models/KundliRecord');

const ADMIN_KEY = process.env.ADMIN_KEY || 'admin@kundli2026';

// Middleware to verify admin key header
const verifyAdmin = (req, res, next) => {
  const clientKey = req.headers['x-admin-key'];
  if (!clientKey || clientKey !== ADMIN_KEY) {
    return res.status(401).json({ detail: 'Unauthorized: Invalid Admin Key' });
  }
  next();
};

/**
 * @route   POST /api/admin/login
 * @desc    Verify admin passcode
 */
router.post('/login', (req, res) => {
  const { passcode } = req.body;
  if (passcode === ADMIN_KEY) {
    return res.json({ status: 'authenticated', admin_key: ADMIN_KEY });
  }
  return res.status(401).json({ detail: 'Invalid admin passcode. Access denied.' });
});

/**
 * @route   GET /api/admin/stats
 * @desc    Aggregate metrics for admin dashboard
 */
router.get('/stats', verifyAdmin, async (req, res) => {
  try {
    const totalUsers = await User.countDocuments();
    const totalRecords = await KundliRecord.countDocuments();

    // Aggregate checks used
    const sumResult = await User.aggregate([
      { $group: { _id: null, total: { $sum: '$checks_used' } } }
    ]);
    const totalChecksUsed = sumResult.length > 0 ? sumResult[0].total : 0;

    // Users reaching limit
    const usersLimitReached = await User.countDocuments({
      $expr: { $gte: ['$checks_used', '$max_limit'] }
    });

    // Records generated today
    const todayPrefix = new Date().toISOString().substring(0, 10);
    const recordsToday = await KundliRecord.countDocuments({
      createdAt: { $regex: `^${todayPrefix}` }
    });

    return res.json({
      total_users: totalUsers,
      total_records: totalRecords,
      total_checks_used: totalChecksUsed,
      users_limit_reached: usersLimitReached,
      records_today: recordsToday,
      default_limit: parseInt(process.env.DEFAULT_CHECK_LIMIT || '10', 10)
    });
  } catch (error) {
    console.error('Error fetching admin stats:', error);
    return res.status(500).json({ detail: error.message });
  }
});

/**
 * @route   GET /api/admin/users
 * @desc    List registered users with search and pagination
 */
router.get('/users', verifyAdmin, async (req, res) => {
  try {
    const search = req.query.search ? req.query.search.trim() : '';
    const limit = parseInt(req.query.limit || '100', 10);
    const offset = parseInt(req.query.offset || '0', 10);

    let query = {};
    if (search) {
      const regex = new RegExp(search, 'i');
      query = {
        $or: [{ name: regex }, { email: regex }, { mobile: regex }]
      };
    }

    const users = await User.find(query)
      .sort({ createdAt: -1 })
      .skip(offset)
      .limit(limit);

    const formattedUsers = users.map((u) => u.toAPIResponse());
    return res.json({ users: formattedUsers, count: formattedUsers.length });
  } catch (error) {
    console.error('Error fetching admin users:', error);
    return res.status(500).json({ detail: error.message });
  }
});

/**
 * @route   GET /api/admin/records
 * @desc    List calculation history with search and pagination
 */
router.get('/records', verifyAdmin, async (req, res) => {
  try {
    const search = req.query.search ? req.query.search.trim() : '';
    const limit = parseInt(req.query.limit || '100', 10);
    const offset = parseInt(req.query.offset || '0', 10);

    let query = {};
    if (search) {
      const regex = new RegExp(search, 'i');
      query = {
        $or: [
          { userName: regex },
          { userEmail: regex },
          { userMobile: regex },
          { seekerName: regex }
        ]
      };
    }

    const records = await KundliRecord.find(query)
      .sort({ _id: -1 })
      .skip(offset)
      .limit(limit);

    const formattedRecords = records.map((r) => r.toAPIResponse());
    return res.json({ records: formattedRecords, count: formattedRecords.length });
  } catch (error) {
    console.error('Error fetching admin records:', error);
    return res.status(500).json({ detail: error.message });
  }
});

/**
 * @route   POST /api/admin/users/:userId/limit
 * @desc    Reset checks or modify limit for a user
 */
router.post('/users/:userId/limit', verifyAdmin, async (req, res) => {
  try {
    const { userId } = req.params;
    const { new_limit, newLimit, reset_checks, resetChecks } = req.body;

    const limitVal = new_limit !== undefined ? new_limit : newLimit;
    const shouldReset = reset_checks !== undefined ? reset_checks : resetChecks;

    const user = await User.findById(userId);
    if (!user) {
      return res.status(404).json({ detail: `User with ID ${userId} not found` });
    }

    if (shouldReset) {
      user.checks_used = 0;
    }
    if (limitVal !== undefined && limitVal !== null) {
      user.max_limit = parseInt(limitVal, 10);
    }

    await user.save();
    return res.json({ status: 'success', user: user.toAPIResponse() });
  } catch (error) {
    console.error('Error adjusting user limit:', error);
    return res.status(500).json({ detail: error.message });
  }
});

module.exports = router;

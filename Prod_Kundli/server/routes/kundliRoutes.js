const express = require('express');
const router = express.Router();
const User = require('../models/User');
const KundliRecord = require('../models/KundliRecord');
const { calculateKundli, calculateMatching } = require('../services/pythonBridge');

/**
 * @route   GET /api/kundli/user-quota
 * @desc    Check current checks used and remaining limit
 */
router.get('/user-quota', async (req, res) => {
  try {
    const { email, mobile, name } = req.query;
    if (!email) {
      return res.status(400).json({ detail: 'Email query parameter is required' });
    }

    const user = await User.findOrCreate({ name, email, mobile });
    return res.json(user.toAPIResponse());
  } catch (error) {
    console.error('Error in /user-quota:', error);
    return res.status(500).json({ detail: error.message });
  }
});

/**
 * @route   POST /api/kundli/generate
 * @desc    Generate Complete Kundli, enforce 10-check quota, and record birth history
 */
router.post('/generate', async (req, res) => {
  try {
    const birthData = req.body;
    let user = null;

    // 1. Quota Verification if user_email provided
    if (birthData.user_email) {
      user = await User.findOrCreate({
        name: birthData.user_name || birthData.name,
        email: birthData.user_email,
        mobile: birthData.user_mobile || ''
      });

      if (user.checks_used >= user.max_limit) {
        return res.status(403).json({
          detail: `Check limit reached (${user.checks_used}/${user.max_limit} Kundlis used). Contact the administrator to increase your limit.`
        });
      }
    }

    // 2. Perform Swiss Ephemeris calculations via Python Bridge
    const report = await calculateKundli(birthData);

    // 3. Atomically increment checks_used and record generation log
    if (user) {
      user.checks_used += 1;
      await user.save();

      const ascSign = report?.ascendant?.sign || '';
      const moonSign = report?.planets?.Moon?.sign || '';
      const nakshatra = report?.planets?.Moon?.nakshatra || '';

      await KundliRecord.create({
        userId: user._id,
        userName: user.name,
        userEmail: user.email,
        userMobile: user.mobile,
        seekerName: birthData.name,
        birthDate: String(birthData.date),
        birthTime: String(birthData.time),
        timezone: birthData.timezone || 'Asia/Kolkata',
        latitude: parseFloat(birthData.latitude),
        longitude: parseFloat(birthData.longitude),
        ayanamsa: birthData.ayanamsa || 'Lahiri',
        houseSystem: birthData.house_system || 'P',
        ascendantSign: ascSign,
        moonSign: moonSign,
        nakshatra: nakshatra
      });

      report.user_quota = user.toAPIResponse();
    }

    return res.json(report);
  } catch (error) {
    console.error('Error generating Kundli:', error);
    return res.status(500).json({ detail: error.message });
  }
});

/**
 * @route   POST /api/kundli/matching
 * @desc    36-Gun Milan Marriage Compatibility
 */
router.post('/matching', async (req, res) => {
  try {
    const { groom, bride } = req.body;
    if (!groom || !bride) {
      return res.status(400).json({ detail: 'Both groom and bride birth parameters are required.' });
    }
    const result = await calculateMatching(groom, bride);
    return res.json(result);
  } catch (error) {
    console.error('Error matching Kundli:', error);
    return res.status(500).json({ detail: error.message });
  }
});

module.exports = router;

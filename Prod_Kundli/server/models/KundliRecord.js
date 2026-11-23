const mongoose = require('mongoose');

const kundliRecordSchema = new mongoose.Schema(
  {
    userId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'User',
      required: true,
      index: true
    },
    userName: { type: String, default: '' },
    userEmail: { type: String, default: '', index: true },
    userMobile: { type: String, default: '' },
    seekerName: { type: String, required: true },
    birthDate: { type: String, required: true },
    birthTime: { type: String, required: true },
    timezone: { type: String, required: true },
    latitude: { type: Number, required: true },
    longitude: { type: Number, required: true },
    ayanamsa: { type: String, default: 'Lahiri' },
    houseSystem: { type: String, default: 'P' },
    ascendantSign: { type: String, default: '' },
    moonSign: { type: String, default: '' },
    nakshatra: { type: String, default: '' },
    createdAt: {
      type: String,
      default: () => new Date().toISOString().replace('T', ' ').substring(0, 19),
      index: true
    }
  },
  {
    timestamps: false
  }
);

kundliRecordSchema.methods.toAPIResponse = function () {
  return {
    id: this._id.toString(),
    user_id: this.userId.toString(),
    user_name: this.userName,
    user_email: this.userEmail,
    user_mobile: this.userMobile,
    seeker_name: this.seekerName,
    birth_date: this.birthDate,
    birth_time: this.birthTime,
    timezone: this.timezone,
    latitude: this.latitude,
    longitude: this.longitude,
    ayanamsa: this.ayanamsa,
    house_system: this.houseSystem,
    ascendant_sign: this.ascendantSign,
    moon_sign: this.moonSign,
    nakshatra: this.nakshatra,
    created_at: this.createdAt
  };
};

module.exports = mongoose.model('KundliRecord', kundliRecordSchema);

const mongoose = require('mongoose');

const userSchema = new mongoose.Schema(
  {
    name: {
      type: String,
      required: true,
      trim: true,
      default: 'Seeker'
    },
    email: {
      type: String,
      required: true,
      trim: true,
      lowercase: true,
      unique: true,
      index: true
    },
    mobile: {
      type: String,
      required: true,
      trim: true,
      index: true
    },
    checks_used: {
      type: Number,
      default: 0
    },
    max_limit: {
      type: Number,
      default: 10
    }
  },
  {
    timestamps: true,
    toJSON: { virtuals: true },
    toObject: { virtuals: true }
  }
);

// Virtual for remaining checks
userSchema.virtual('remaining_checks').get(function () {
  return Math.max(0, this.max_limit - this.checks_used);
});

// Virtual for quota availability
userSchema.virtual('has_quota').get(function () {
  return this.remaining_checks > 0;
});

// Format output for API & frontend compatibility
userSchema.methods.toAPIResponse = function () {
  return {
    id: this._id.toString(),
    user_name: this.name,
    user_email: this.email,
    user_mobile: this.mobile,
    checks_used: this.checks_used,
    max_limit: this.max_limit,
    remaining_checks: this.remaining_checks,
    has_quota: this.has_quota,
    created_at: this.createdAt,
    updated_at: this.updatedAt
  };
};

// Static helper to find or create user
userSchema.statics.findOrCreate = async function ({ name, email, mobile }) {
  const cleanEmail = email.trim().toLowerCase();
  const cleanMobile = mobile ? mobile.trim() : '';
  const cleanName = (name && name.trim()) || 'Seeker';

  let user = await this.findOne({ email: cleanEmail });
  if (user) {
    let updated = false;
    if (cleanName && cleanName !== 'Seeker' && user.name !== cleanName) {
      user.name = cleanName;
      updated = true;
    }
    if (cleanMobile && user.mobile !== cleanMobile) {
      user.mobile = cleanMobile;
      updated = true;
    }
    if (updated) {
      await user.save();
    }
    return user;
  }

  user = await this.create({
    name: cleanName,
    email: cleanEmail,
    mobile: cleanMobile,
    checks_used: 0,
    max_limit: parseInt(process.env.DEFAULT_CHECK_LIMIT || '10', 10)
  });
  return user;
};

module.exports = mongoose.model('User', userSchema);

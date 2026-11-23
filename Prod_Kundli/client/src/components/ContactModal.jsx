import React, { useState } from 'react';

export default function ContactModal({ isOpen, onClose, onConfirm, seekerName, birthDate, birthTime, initialUser, userQuota, loading }) {
  if (!isOpen) return null;

  const [userName, setUserName] = useState(initialUser?.user_name || localStorage.getItem('kundli_user_name') || '');
  const [userEmail, setUserEmail] = useState(initialUser?.user_email || localStorage.getItem('kundli_user_email') || '');
  const [userMobile, setUserMobile] = useState(initialUser?.user_mobile || localStorage.getItem('kundli_user_mobile') || '');
  const [error, setError] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    setError('');

    const cleanName = userName.trim();
    const cleanEmail = userEmail.trim().toLowerCase();
    const cleanMobile = userMobile.trim();

    if (!cleanName) {
      setError('Please enter your full name');
      return;
    }
    if (!cleanEmail || !cleanEmail.includes('@')) {
      setError('Please enter a valid email address');
      return;
    }
    if (!cleanMobile || cleanMobile.length < 7) {
      setError('Please enter a valid mobile number');
      return;
    }

    // Persist to localStorage
    localStorage.setItem('kundli_user_name', cleanName);
    localStorage.setItem('kundli_user_email', cleanEmail);
    localStorage.setItem('kundli_user_mobile', cleanMobile);

    onConfirm({
      user_name: cleanName,
      user_email: cleanEmail,
      user_mobile: cleanMobile
    });
  };

  return (
    <div className="fixed inset-0 bg-stone-900/65 backdrop-blur-xs flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-2xl max-w-md w-full shadow-2xl border border-amber-200 overflow-hidden animate-in fade-in zoom-in-95 duration-200">
        {/* Header */}
        <div className="card-header-vedic px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <span className="text-2xl">🕉️</span>
            <div>
              <h3 className="font-bold text-amber-950 text-base vedic-title">
                Enter Contact Information
              </h3>
              <p className="text-[11px] text-amber-800 font-medium">
                {userQuota
                  ? `${userQuota.remaining_checks} of ${userQuota.max_limit} Kundli checks remaining`
                  : '10 Free Kundli Checks per User Account'}
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="text-stone-400 hover:text-stone-700 text-lg font-bold p-1 rounded-lg transition"
          >
            ✕
          </button>
        </div>

        {/* Body */}
        <div className="p-6 space-y-4">
          {/* Target Chart Summary */}
          <div className="p-3 bg-amber-50/70 border border-amber-200/80 rounded-xl text-xs space-y-1">
            <span className="text-[10px] uppercase font-bold text-amber-800 tracking-wider block">
              Generating Kundli For
            </span>
            <div className="font-bold text-stone-800 text-sm">
              {seekerName || 'Seeker'}
            </div>
            <div className="text-stone-600 font-mono text-[11px]">
              📅 {birthDate} at ⏰ {birthTime}
            </div>
          </div>

          <form onSubmit={handleSubmit} className="space-y-3.5">
            <div>
              <label className="block text-xs font-semibold text-stone-700 mb-1">
                Your Full Name <span className="text-rose-500">*</span>
              </label>
              <input
                type="text"
                value={userName}
                onChange={e => setUserName(e.target.value)}
                placeholder="e.g. Rahul Sharma"
                className="w-full px-3 py-2 border border-amber-200 rounded-lg text-sm bg-stone-50 focus:bg-white focus:outline-none focus:ring-2 focus:ring-amber-500"
                required
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-stone-700 mb-1">
                Email Address <span className="text-rose-500">*</span>
              </label>
              <input
                type="email"
                value={userEmail}
                onChange={e => setUserEmail(e.target.value)}
                placeholder="rahul@example.com"
                className="w-full px-3 py-2 border border-amber-200 rounded-lg text-sm bg-stone-50 focus:bg-white focus:outline-none focus:ring-2 focus:ring-amber-500"
                required
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-stone-700 mb-1">
                Mobile Number <span className="text-rose-500">*</span>
              </label>
              <input
                type="tel"
                value={userMobile}
                onChange={e => setUserMobile(e.target.value)}
                placeholder="+91 9876543210"
                className="w-full px-3 py-2 border border-amber-200 rounded-lg text-sm bg-stone-50 focus:bg-white focus:outline-none focus:ring-2 focus:ring-amber-500"
                required
              />
            </div>

            {error && (
              <p className="text-xs text-rose-600 font-semibold bg-rose-50 p-2 rounded border border-rose-200">
                ⚠️ {error}
              </p>
            )}

            <div className="pt-2 flex gap-2.5">
              <button
                type="button"
                onClick={onClose}
                className="w-1/3 py-2.5 px-3 rounded-xl border border-stone-200 text-stone-700 font-bold text-xs hover:bg-stone-100 transition cursor-pointer"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={loading}
                className="w-2/3 py-2.5 px-4 rounded-xl bg-gradient-to-r from-amber-600 to-amber-700 hover:from-amber-700 hover:to-amber-800 text-white font-bold text-xs uppercase tracking-wider shadow-md transition cursor-pointer flex items-center justify-center gap-1.5 disabled:opacity-50"
              >
                {loading ? (
                  <span>Calculating Kundli...</span>
                ) : (
                  <>
                    <span>✨</span>
                    <span>Submit & Generate</span>
                  </>
                )}
              </button>
            </div>
          </form>

          <p className="text-[11px] text-stone-500 text-center">
            🔒 Your contact details are stored securely for quota tracking & admin records.
          </p>
        </div>
      </div>
    </div>
  );
}

import React from 'react';

const CITY_PRESETS = [
  { name: "Agra, India", lat: 27.1767, lon: 78.0081, tz: "Asia/Kolkata" },
  { name: "New Delhi, India", lat: 28.6139, lon: 77.2090, tz: "Asia/Kolkata" },
  { name: "Mumbai, India", lat: 19.0760, lon: 72.8777, tz: "Asia/Kolkata" },
  { name: "Bengaluru, India", lat: 12.9716, lon: 77.5946, tz: "Asia/Kolkata" },
  { name: "Varanasi, India", lat: 25.3176, lon: 82.9739, tz: "Asia/Kolkata" },
  { name: "London, UK", lat: 51.5074, lon: -0.1278, tz: "Europe/London" },
  { name: "New York, USA", lat: 40.7128, lon: -74.0060, tz: "America/New_York" },
  { name: "Tokyo, Japan", lat: 35.6762, lon: 139.6503, tz: "Asia/Tokyo" }
];

export default function BirthForm({ formData, setFormData, onOpenContactModal, loading, userQuota }) {
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: (name === 'latitude' || name === 'longitude') ? parseFloat(value) || 0 : value
    }));
  };

  const handleCitySelect = (city) => {
    setFormData(prev => ({
      ...prev,
      latitude: city.lat,
      longitude: city.lon,
      timezone: city.tz
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Open the contact info pop-up modal first before executing Kundli!
    onOpenContactModal();
  };

  const isLimitExhausted = userQuota && userQuota.remaining_checks <= 0;

  return (
    <div className="card-vedic p-5 space-y-4">
      {/* User Status / Quota Banner */}
      <div className="p-3 bg-gradient-to-r from-amber-50 to-orange-50/70 rounded-xl border border-amber-200 flex flex-wrap items-center justify-between gap-2">
        <div className="flex items-center gap-2">
          <span className="text-lg">👤</span>
          <div>
            <div className="text-xs font-bold text-amber-950">
              {formData.user_email ? (
                <>User: <span className="text-amber-800">{formData.user_name || 'Registered User'}</span> ({formData.user_email})</>
              ) : (
                'Free Kundli Access'
              )}
            </div>
            <div className="text-[11px] text-stone-500">
              10 Free Kundli Checks per user account
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2">
          {userQuota ? (
            <span className={`text-xs font-black px-2.5 py-1 rounded-full ${
              userQuota.remaining_checks > 0
                ? 'bg-amber-200 text-amber-950 border border-amber-300'
                : 'bg-rose-200 text-rose-900 border border-rose-300'
            }`}>
              {userQuota.remaining_checks} of {userQuota.max_limit} Checks Left
            </span>
          ) : (
            <span className="text-xs font-bold bg-amber-100 text-amber-900 px-2.5 py-1 rounded-full border border-amber-200">
              10 Free Checks
            </span>
          )}
          <button
            type="button"
            onClick={onOpenContactModal}
            className="text-[11px] text-amber-900 hover:text-amber-700 underline font-semibold transition"
          >
            {formData.user_email ? 'Change' : 'Set Contact'}
          </button>
        </div>
      </div>

      {isLimitExhausted && (
        <div className="p-3 bg-rose-100 border border-rose-300 text-rose-900 text-xs font-semibold rounded-xl flex items-center gap-2">
          <span>⚠️</span> You have exhausted your 10 Kundli checks for this account. Please contact the administrator to reset or increase your quota.
        </div>
      )}

      <div className="flex items-center gap-2 border-b border-amber-100 pb-2">
        <span className="text-xl">📜</span>
        <h2 className="text-lg font-bold text-amber-900 vedic-title">Seeker Birth Details (Janma Vivarana)</h2>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Seeker Name */}
        <div>
          <label className="block text-xs font-semibold text-amber-900 uppercase tracking-wider mb-1">
            Seeker / Native Name *
          </label>
          <input
            type="text"
            name="name"
            value={formData.name}
            onChange={handleChange}
            className="w-full px-3 py-2 border border-amber-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-amber-500 bg-white"
            placeholder="Person whose birth chart is being calculated"
            required
          />
        </div>

        {/* Date & Time */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div>
            <label className="block text-xs font-semibold text-amber-900 uppercase tracking-wider mb-1">
              Birth Date *
            </label>
            <input
              type="date"
              name="date"
              value={formData.date}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-amber-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-amber-500 bg-white"
              required
            />
          </div>
          <div>
            <label className="block text-xs font-semibold text-amber-900 uppercase tracking-wider mb-1">
              Birth Time (24h) *
            </label>
            <input
              type="time"
              step="1"
              name="time"
              value={formData.time}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-amber-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-amber-500 bg-white"
              required
            />
          </div>
        </div>

        {/* City Presets */}
        <div>
          <label className="block text-xs font-semibold text-amber-800 mb-1">Quick City Presets</label>
          <div className="flex flex-wrap gap-1.5">
            {CITY_PRESETS.map((c) => (
              <button
                key={c.name}
                type="button"
                onClick={() => handleCitySelect(c)}
                className="text-xs px-2.5 py-1 bg-amber-100/70 hover:bg-amber-200 text-amber-900 rounded-md transition font-medium cursor-pointer"
              >
                {c.name.split(',')[0]}
              </button>
            ))}
          </div>
        </div>

        {/* Coordinates & Timezone */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <div>
            <label className="block text-xs font-semibold text-amber-900 uppercase tracking-wider mb-1">Latitude</label>
            <input
              type="number"
              step="any"
              name="latitude"
              value={formData.latitude}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-amber-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-amber-500 bg-white"
              required
            />
          </div>
          <div>
            <label className="block text-xs font-semibold text-amber-900 uppercase tracking-wider mb-1">Longitude</label>
            <input
              type="number"
              step="any"
              name="longitude"
              value={formData.longitude}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-amber-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-amber-500 bg-white"
              required
            />
          </div>
          <div>
            <label className="block text-xs font-semibold text-amber-900 uppercase tracking-wider mb-1">Timezone</label>
            <input
              type="text"
              name="timezone"
              value={formData.timezone}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-amber-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-amber-500 bg-white"
              required
            />
          </div>
        </div>

        {/* Ayanamsa & House System */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <div>
            <label className="block text-xs font-semibold text-amber-900 uppercase tracking-wider mb-1">Ayanamsa</label>
            <select
              name="ayanamsa"
              value={formData.ayanamsa}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-amber-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-amber-500 bg-white"
            >
              <option value="Lahiri">Lahiri (Chitra Paksha)</option>
              <option value="KP">KP (Krishnamurti)</option>
              <option value="Raman">B.V. Raman</option>
              <option value="Yukteshwar">Sri Yukteshwar</option>
              <option value="Fagan_Bradley">Fagan-Bradley</option>
              <option value="Sayana">Sayana (Tropical)</option>
            </select>
          </div>
          <div>
            <label className="block text-xs font-semibold text-amber-900 uppercase tracking-wider mb-1">House System</label>
            <select
              name="house_system"
              value={formData.house_system}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-amber-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-amber-500 bg-white"
            >
              <option value="P">Placidus (Standard for KP)</option>
              <option value="W">Whole Sign (Vedic Parashari)</option>
              <option value="E">Equal House</option>
              <option value="S">Sripati / Porphyry</option>
            </select>
          </div>
          <div>
            <label className="block text-xs font-semibold text-amber-900 uppercase tracking-wider mb-1">Rahu/Ketu Mode</label>
            <select
              name="node_type"
              value={formData.node_type}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-amber-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-amber-500 bg-white"
            >
              <option value="mean">Mean Nodes (Traditional)</option>
              <option value="true">True Nodes (Astronomical)</option>
            </select>
          </div>
        </div>

        {/* Generate Button */}
        <button
          type="submit"
          disabled={loading || isLimitExhausted}
          className="w-full py-3 bg-gradient-to-r from-amber-600 to-amber-700 hover:from-amber-700 hover:to-amber-800 text-white font-bold rounded-xl shadow-md transition duration-200 flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50 text-sm tracking-wide"
        >
          {loading ? (
            <>
              <svg className="animate-spin h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
              </svg>
              <span>Calculating Planetary Positions...</span>
            </>
          ) : (
            <>
              <span>✨</span>
              <span>Generate Vedic & KP Kundli</span>
            </>
          )}
        </button>
      </form>
    </div>
  );
}

import React, { useState, useEffect } from 'react';
import { adminLogin, fetchAdminStats, fetchAdminUsers, fetchAdminRecords, adjustUserLimit } from '../api/adminApi';

export default function AdminPanel({ onClose }) {
  const [adminKey, setAdminKey] = useState(localStorage.getItem('kundli_admin_key') || '');
  const [passcode, setPasscode] = useState('');
  const [isAuthenticated, setIsAuthenticated] = useState(!!adminKey);
  const [loginError, setLoginError] = useState('');
  
  const [stats, setStats] = useState(null);
  const [users, setUsers] = useState([]);
  const [records, setRecords] = useState([]);
  const [activeTab, setActiveTab] = useState('users'); // 'users' or 'records'
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [actionMessage, setActionMessage] = useState('');

  // Limit edit modal state
  const [selectedUser, setSelectedUser] = useState(null);
  const [newLimitInput, setNewLimitInput] = useState(10);
  const [resetChecksBox, setResetChecksBox] = useState(false);

  useEffect(() => {
    if (isAuthenticated && adminKey) {
      loadData();
    }
  }, [isAuthenticated, adminKey]);

  const loadData = async (query = '') => {
    setLoading(true);
    try {
      const [sData, uData, rData] = await Promise.all([
        fetchAdminStats(adminKey),
        fetchAdminUsers(adminKey, query),
        fetchAdminRecords(adminKey, query)
      ]);
      setStats(sData);
      setUsers(uData.users);
      setRecords(rData.records);
    } catch (err) {
      if (err.message.includes('Unauthorized')) {
        setIsAuthenticated(false);
        localStorage.removeItem('kundli_admin_key');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoginError('');
    try {
      const res = await adminLogin(passcode);
      setAdminKey(res.admin_key);
      localStorage.setItem('kundli_admin_key', res.admin_key);
      setIsAuthenticated(true);
    } catch (err) {
      setLoginError(err.message || 'Invalid passcode');
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('kundli_admin_key');
    setAdminKey('');
    setIsAuthenticated(false);
  };

  const handleSearch = (e) => {
    e.preventDefault();
    loadData(searchQuery);
  };

  const handleQuickReset = async (user) => {
    if (!window.confirm(`Reset Kundli checks for ${user.name} (${user.email}) back to 0/${user.max_limit}?`)) return;
    try {
      await adjustUserLimit(adminKey, user.id, { newLimit: user.max_limit, resetChecks: true });
      setActionMessage(`Limit successfully reset for ${user.name}`);
      setTimeout(() => setActionMessage(''), 3000);
      loadData(searchQuery);
    } catch (err) {
      alert(err.message);
    }
  };

  const handleSaveLimitModal = async (e) => {
    e.preventDefault();
    if (!selectedUser) return;
    try {
      await adjustUserLimit(adminKey, selectedUser.id, {
        newLimit: parseInt(newLimitInput, 10),
        resetChecks: resetChecksBox
      });
      setSelectedUser(null);
      setActionMessage(`Updated limit for ${selectedUser.name}`);
      setTimeout(() => setActionMessage(''), 3000);
      loadData(searchQuery);
    } catch (err) {
      alert(err.message);
    }
  };

  const exportRecordsCSV = () => {
    if (!records.length) return;
    const headers = ["ID", "Timestamp", "User Name", "User Email", "User Mobile", "Seeker Name", "Birth Date", "Birth Time", "Latitude", "Longitude", "Timezone", "Ayanamsa", "Ascendant", "Moon Sign", "Nakshatra"];
    const rows = records.map(r => [
      r.id,
      `"${r.created_at}"`,
      `"${r.user_name || ''}"`,
      `"${r.user_email || ''}"`,
      `"${r.user_mobile || ''}"`,
      `"${r.seeker_name}"`,
      r.birth_date,
      r.birth_time,
      r.latitude,
      r.longitude,
      `"${r.timezone}"`,
      r.ayanamsa,
      `"${r.ascendant_sign || ''}"`,
      `"${r.moon_sign || ''}"`,
      `"${r.nakshatra || ''}"`
    ]);

    const csvContent = "data:text/csv;charset=utf-8," + [headers.join(','), ...rows.map(e => e.join(','))].join('\n');
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", `kundli_records_${new Date().toISOString().slice(0, 10)}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  if (!isAuthenticated) {
    return (
      <div className="fixed inset-0 bg-stone-900/60 backdrop-blur-xs flex items-center justify-center p-4 z-50">
        <div className="bg-white rounded-2xl p-6 max-w-md w-full shadow-2xl border border-amber-200">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg font-bold text-amber-900 vedic-title flex items-center gap-2">
              <span>🔒</span> Admin Access
            </h3>
            <button onClick={onClose} className="text-stone-400 hover:text-stone-600 text-lg">✕</button>
          </div>
          <p className="text-xs text-stone-600 mb-4">
            Enter the admin passcode to access user management, quota controls, and historical birth generation records.
          </p>
          <form onSubmit={handleLogin} className="space-y-3">
            <div>
              <label className="text-xs font-semibold text-stone-700 block mb-1">Passcode</label>
              <input
                type="password"
                value={passcode}
                onChange={e => setPasscode(e.target.value)}
                placeholder="Default: admin@kundli2026"
                className="w-full px-3 py-2 border border-amber-200 rounded-lg text-sm bg-stone-50 focus:bg-white focus:outline-none focus:ring-2 focus:ring-amber-500"
                required
              />
            </div>
            {loginError && <p className="text-xs text-red-600 font-semibold">{loginError}</p>}
            <div className="flex gap-2 pt-2">
              <button
                type="button"
                onClick={onClose}
                className="w-1/2 py-2 text-xs font-bold text-stone-600 bg-stone-100 hover:bg-stone-200 rounded-lg transition"
              >
                Cancel
              </button>
              <button
                type="submit"
                className="w-1/2 py-2 text-xs font-bold text-white bg-amber-700 hover:bg-amber-800 rounded-lg shadow-sm transition"
              >
                Authenticate
              </button>
            </div>
          </form>
        </div>
      </div>
    );
  }

  return (
    <div className="fixed inset-0 bg-stone-900/70 backdrop-blur-xs flex items-center justify-center p-3 sm:p-6 z-50 overflow-y-auto">
      <div className="bg-white rounded-2xl w-full max-w-6xl shadow-2xl border border-amber-200 flex flex-col max-h-[92vh] overflow-hidden">
        {/* Header */}
        <div className="card-header-vedic px-6 py-4 flex flex-wrap items-center justify-between gap-3 shrink-0">
          <div className="flex items-center gap-3">
            <span className="text-2xl">🛡️</span>
            <div>
              <h2 className="text-xl font-bold text-amber-950 vedic-title">Kundli Engine Admin Portal</h2>
              <p className="text-xs text-amber-800 font-medium">User limit management, contact leads & birth data audit</p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <button
              onClick={exportRecordsCSV}
              className="text-xs bg-emerald-700 hover:bg-emerald-800 text-white font-bold px-3 py-1.5 rounded-lg shadow-xs flex items-center gap-1.5 transition"
            >
              <span>📥</span> Export CSV
            </button>
            <button
              onClick={handleLogout}
              className="text-xs bg-amber-200/80 hover:bg-amber-300 text-amber-950 font-bold px-3 py-1.5 rounded-lg transition"
            >
              Logout
            </button>
            <button
              onClick={onClose}
              className="text-stone-500 hover:text-stone-800 font-bold text-lg px-2"
            >
              ✕
            </button>
          </div>
        </div>

        {/* Action message banner */}
        {actionMessage && (
          <div className="bg-emerald-100 border-b border-emerald-200 px-6 py-2 text-xs font-bold text-emerald-800 text-center">
            {actionMessage}
          </div>
        )}

        {/* Content Body */}
        <div className="p-6 overflow-y-auto space-y-6 flex-1">
          {/* KPI Summary Cards */}
          {stats && (
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-3">
              <div className="bg-amber-50/70 p-3.5 rounded-xl border border-amber-200 text-center">
                <span className="text-xs uppercase font-semibold text-amber-800 block">Total Users</span>
                <span className="text-2xl font-black text-amber-950 mt-1 block">{stats.total_users}</span>
              </div>
              <div className="bg-blue-50/70 p-3.5 rounded-xl border border-blue-200 text-center">
                <span className="text-xs uppercase font-semibold text-blue-800 block">Total Kundlis</span>
                <span className="text-2xl font-black text-blue-950 mt-1 block">{stats.total_records}</span>
              </div>
              <div className="bg-emerald-50/70 p-3.5 rounded-xl border border-emerald-200 text-center">
                <span className="text-xs uppercase font-semibold text-emerald-800 block">Generated Today</span>
                <span className="text-2xl font-black text-emerald-950 mt-1 block">{stats.records_today}</span>
              </div>
              <div className="bg-purple-50/70 p-3.5 rounded-xl border border-purple-200 text-center">
                <span className="text-xs uppercase font-semibold text-purple-800 block">Total Checks Used</span>
                <span className="text-2xl font-black text-purple-950 mt-1 block">{stats.total_checks_used}</span>
              </div>
              <div className="bg-rose-50/70 p-3.5 rounded-xl border border-rose-200 text-center">
                <span className="text-xs uppercase font-semibold text-rose-800 block">At Limit (10/10)</span>
                <span className="text-2xl font-black text-rose-950 mt-1 block">{stats.users_limit_reached}</span>
              </div>
            </div>
          )}

          {/* Search & Tabs Toolbar */}
          <div className="flex flex-wrap items-center justify-between gap-3 border-b border-amber-100 pb-3">
            <div className="flex bg-amber-100/70 p-1 rounded-xl text-xs font-bold">
              <button
                onClick={() => setActiveTab('users')}
                className={`px-4 py-2 rounded-lg transition ${activeTab === 'users' ? 'bg-amber-800 text-white shadow-xs' : 'text-amber-950 hover:bg-amber-200'}`}
              >
                👥 Users & Limit Controls ({users.length})
              </button>
              <button
                onClick={() => setActiveTab('records')}
                className={`px-4 py-2 rounded-lg transition ${activeTab === 'records' ? 'bg-amber-800 text-white shadow-xs' : 'text-amber-950 hover:bg-amber-200'}`}
              >
                📜 Birth Information Audit Log ({records.length})
              </button>
            </div>

            <form onSubmit={handleSearch} className="flex gap-2 w-full sm:w-auto">
              <input
                type="text"
                placeholder="Search name, email, or mobile..."
                value={searchQuery}
                onChange={e => setSearchQuery(e.target.value)}
                className="px-3 py-1.5 border border-amber-200 rounded-lg text-xs bg-white focus:outline-none focus:ring-2 focus:ring-amber-500 w-full sm:w-64"
              />
              <button
                type="submit"
                className="px-3 py-1.5 bg-amber-700 hover:bg-amber-800 text-white font-bold text-xs rounded-lg transition"
              >
                Search
              </button>
              {searchQuery && (
                <button
                  type="button"
                  onClick={() => { setSearchQuery(''); loadData(''); }}
                  className="px-2.5 py-1.5 bg-stone-200 hover:bg-stone-300 text-stone-700 font-bold text-xs rounded-lg transition"
                >
                  Clear
                </button>
              )}
            </form>
          </div>

          {/* Tab 1: Users & Check Limit Management */}
          {activeTab === 'users' && (
            <div className="overflow-x-auto">
              <table className="vedic-table">
                <thead>
                  <tr>
                    <th>User ID</th>
                    <th>User Name</th>
                    <th>Email Address</th>
                    <th>Mobile Number</th>
                    <th>Checks Status</th>
                    <th>Registration Date</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {users.map((u) => {
                    const isLimitReached = u.checks_used >= u.max_limit;
                    const pct = Math.min(100, (u.checks_used / u.max_limit) * 100);
                    return (
                      <tr key={u.id}>
                        <td className="font-mono text-xs text-stone-500">#{u.id}</td>
                        <td className="font-bold text-amber-950 text-sm">{u.name}</td>
                        <td className="font-mono text-xs text-stone-700">{u.email}</td>
                        <td className="font-mono text-xs text-stone-700">{u.mobile || '-'}</td>
                        <td className="w-48">
                          <div className="flex items-center justify-between text-xs mb-1">
                            <span className={`font-bold ${isLimitReached ? 'text-rose-700' : 'text-stone-700'}`}>
                              {u.checks_used} / {u.max_limit} Used
                            </span>
                            <span className="text-[11px] text-stone-500">
                              ({u.remaining_checks} left)
                            </span>
                          </div>
                          <div className="w-full bg-stone-200 h-2 rounded-full overflow-hidden">
                            <div
                              className={`h-full ${isLimitReached ? 'bg-rose-500' : pct > 60 ? 'bg-amber-500' : 'bg-emerald-500'}`}
                              style={{ width: `${pct}%` }}
                            />
                          </div>
                        </td>
                        <td className="text-xs text-stone-500 font-mono">
                          {u.created_at ? u.created_at.replace('T', ' ').slice(0, 19) : '-'}
                        </td>
                        <td>
                          <div className="flex items-center gap-1.5">
                            <button
                              onClick={() => handleQuickReset(u)}
                              title="Reset checks used to 0"
                              className="px-2.5 py-1 bg-amber-100 hover:bg-amber-200 text-amber-900 rounded font-bold text-xs transition"
                            >
                              Reset
                            </button>
                            <button
                              onClick={() => {
                                setSelectedUser(u);
                                setNewLimitInput(u.max_limit + 10);
                                setResetChecksBox(false);
                              }}
                              title="Adjust maximum check quota"
                              className="px-2.5 py-1 bg-stone-100 hover:bg-stone-200 text-stone-800 rounded font-semibold text-xs transition"
                            >
                              Edit Limit
                            </button>
                          </div>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          )}

          {/* Tab 2: Full Birth Data Records Audit Log */}
          {activeTab === 'records' && (
            <div className="overflow-x-auto">
              <table className="vedic-table text-xs">
                <thead>
                  <tr>
                    <th>Timestamp</th>
                    <th>User Contact</th>
                    <th>Seeker / Native Name</th>
                    <th>Birth Date & Time</th>
                    <th>Birth Location</th>
                    <th>Ayanamsa</th>
                    <th>Calculated Signs</th>
                  </tr>
                </thead>
                <tbody>
                  {records.map((r) => (
                    <tr key={r.id}>
                      <td className="font-mono text-[11px] text-stone-500 whitespace-nowrap">
                        {r.created_at}
                      </td>
                      <td>
                        <span className="font-bold text-stone-900 block">{r.user_name || 'Anonymous'}</span>
                        <span className="text-stone-600 block">{r.user_email}</span>
                        <span className="text-stone-500 block font-mono">{r.user_mobile || '-'}</span>
                      </td>
                      <td>
                        <span className="font-bold text-amber-950 text-sm">{r.seeker_name}</span>
                      </td>
                      <td>
                        <span className="font-semibold text-stone-800 block">{r.birth_date}</span>
                        <span className="text-stone-500 font-mono block">{r.birth_time}</span>
                      </td>
                      <td>
                        <span className="font-mono text-stone-700 block">{r.latitude.toFixed(4)}°, {r.longitude.toFixed(4)}°</span>
                        <span className="text-[11px] text-stone-500 block">{r.timezone}</span>
                      </td>
                      <td>
                        <span className="bg-amber-100 text-amber-900 px-1.5 py-0.5 rounded font-semibold text-[11px]">
                          {r.ayanamsa}
                        </span>
                      </td>
                      <td>
                        <span className="text-stone-700 block">Lagna: <strong>{r.ascendant_sign || '-'}</strong></span>
                        <span className="text-stone-700 block">Moon: <strong>{r.moon_sign || '-'}</strong> ({r.nakshatra || '-'})</span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>

        {/* Modal: Adjust User Limit */}
        {selectedUser && (
          <div className="fixed inset-0 bg-stone-900/60 backdrop-blur-xs flex items-center justify-center p-4 z-60">
            <div className="bg-white rounded-xl p-5 max-w-sm w-full shadow-2xl border border-amber-200">
              <div className="flex justify-between items-center mb-3">
                <h4 className="font-bold text-amber-900 text-sm">Adjust Limit: {selectedUser.name}</h4>
                <button onClick={() => setSelectedUser(null)} className="text-stone-400 hover:text-stone-600">✕</button>
              </div>
              <p className="text-xs text-stone-600 mb-3">
                Current usage: <strong>{selectedUser.checks_used} / {selectedUser.max_limit}</strong>
              </p>
              <form onSubmit={handleSaveLimitModal} className="space-y-3">
                <div>
                  <label className="text-xs font-semibold text-stone-700 block mb-1">New Max Limit</label>
                  <input
                    type="number"
                    min="1"
                    max="1000"
                    value={newLimitInput}
                    onChange={e => setNewLimitInput(e.target.value)}
                    className="w-full px-3 py-1.5 border border-amber-200 rounded text-sm bg-white"
                    required
                  />
                </div>
                <div className="flex items-center gap-2">
                  <input
                    type="checkbox"
                    id="resetChecksBox"
                    checked={resetChecksBox}
                    onChange={e => setResetChecksBox(e.target.checked)}
                    className="rounded text-amber-600 focus:ring-amber-500"
                  />
                  <label htmlFor="resetChecksBox" className="text-xs text-stone-700 font-medium cursor-pointer">
                    Also reset used checks back to 0
                  </label>
                </div>
                <div className="flex gap-2 pt-2">
                  <button
                    type="button"
                    onClick={() => setSelectedUser(null)}
                    className="w-1/2 py-2 text-xs font-bold text-stone-600 bg-stone-100 rounded"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    className="w-1/2 py-2 text-xs font-bold text-white bg-amber-700 rounded shadow-xs"
                  >
                    Save Quota
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

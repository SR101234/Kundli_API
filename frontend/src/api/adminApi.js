const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

export async function adminLogin(passcode) {
  const res = await fetch(`${BASE_URL}/api/admin/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ passcode }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Invalid admin passcode');
  }
  return res.json();
}

export async function fetchAdminStats(adminKey) {
  const res = await fetch(`${BASE_URL}/api/admin/stats`, {
    headers: { 'X-Admin-Key': adminKey }
  });
  if (!res.ok) throw new Error('Failed to fetch admin stats');
  return res.json();
}

export async function fetchAdminUsers(adminKey, search = '') {
  const url = search 
    ? `${BASE_URL}/api/admin/users?search=${encodeURIComponent(search)}`
    : `${BASE_URL}/api/admin/users`;
  const res = await fetch(url, {
    headers: { 'X-Admin-Key': adminKey }
  });
  if (!res.ok) throw new Error('Failed to fetch users');
  return res.json();
}

export async function fetchAdminRecords(adminKey, search = '') {
  const url = search
    ? `${BASE_URL}/api/admin/records?search=${encodeURIComponent(search)}`
    : `${BASE_URL}/api/admin/records`;
  const res = await fetch(url, {
    headers: { 'X-Admin-Key': adminKey }
  });
  if (!res.ok) throw new Error('Failed to fetch records');
  return res.json();
}

export async function adjustUserLimit(adminKey, userId, { newLimit, resetChecks }) {
  const res = await fetch(`${BASE_URL}/api/admin/users/${userId}/limit`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-Admin-Key': adminKey
    },
    body: JSON.stringify({ new_limit: newLimit, reset_checks: resetChecks })
  });
  if (!res.ok) throw new Error('Failed to adjust user limit');
  return res.json();
}

export async function fetchUserQuota(email, mobile = '', name = '') {
  const res = await fetch(`${BASE_URL}/api/kundli/user-quota?email=${encodeURIComponent(email)}&mobile=${encodeURIComponent(mobile)}&name=${encodeURIComponent(name)}`);
  if (!res.ok) throw new Error('Failed to fetch user quota');
  return res.json();
}

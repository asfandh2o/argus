const API_BASE = '';

function getToken() {
  return localStorage.getItem('argus_token');
}

async function request(path, options = {}) {
  const token = getToken();
  const headers = {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...options.headers,
  };

  const res = await fetch(`${API_BASE}${path}`, { ...options, headers });

  if (res.status === 401) {
    localStorage.removeItem('argus_token');
    localStorage.removeItem('argus_user');
    window.location.href = '/login';
    return;
  }

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || 'Request failed');
  }

  if (res.status === 204) return null;
  return res.json();
}

export const api = {
  // Auth
  adminLogin: (email, password) =>
    request('/auth/login', { method: 'POST', body: JSON.stringify({ email, password }) }),
  employeeLogin: (email) =>
    request('/auth/employee-login', { method: 'POST', body: JSON.stringify({ email }) }),

  // Employees
  listEmployees: () => request('/employees/'),

  // Scores
  myScores: (limit = 30) => request(`/scores/me?limit=${limit}`),
  employeeScores: (id, limit = 30) => request(`/scores/${id}?limit=${limit}`),
  teamSummary: () => request('/scores/team/summary'),

  // Advice
  myAdvice: () => request('/advice/me'),
  employeeAdvice: (id) => request(`/advice/${id}`),
  dismissAdvice: (id) => request(`/advice/${id}/dismiss`, { method: 'PATCH' }),

  // Dashboard
  teamStats: () => request('/dashboard/team-stats'),
};

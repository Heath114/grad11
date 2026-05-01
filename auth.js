// ─── API Configuration ────────────────────────────────────────────────────────
const API_BASE = window.location.origin.includes('127.0.0.1:5500')
    ? 'http://127.0.0.1:5001'
    : window.location.origin;

// ─── Core API helper ──────────────────────────────────────────────────────────
async function apiCall(endpoint, method = 'GET', body = null) {
    const options = {
        method,
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' }
    };
    if (body) options.body = JSON.stringify(body);

    const res  = await fetch(`${API_BASE}${endpoint}`, options);
    const data = await res.json();
    return { ok: res.ok, status: res.status, data };
}

// ─── Auth functions ───────────────────────────────────────────────────────────
async function register(name, lastName, phone, password) {
    const { ok, data } = await apiCall('/auth/register', 'POST', {
        name, lastName, phone, password
    });
    return { success: ok, message: data.message };
}

async function registerAdmin(username, password, cafeteriaId) {
    const { ok, data } = await apiCall('/auth/register-admin', 'POST', {
        username, password, cafeteriaId
    });
    return { success: ok, message: data.message };
}

async function login(username, password) {
    const { ok, data } = await apiCall('/auth/login', 'POST', { username, password });
    if (ok) {
        sessionStorage.setItem('userType',     data.userType);
        sessionStorage.setItem('userName',     data.name       || data.username || '');
        sessionStorage.setItem('userLastName', data.lastName   || '');
        sessionStorage.setItem('userPhone',    data.phone      || '');
        sessionStorage.setItem('userId',       data.userId     || '');

        if (data.userType === 'admin') {
            sessionStorage.setItem('cafeteriaId',   data.cafeteriaId);
            sessionStorage.setItem('cafeteriaName', data.cafeteriaName);
        }
    }
    return { success: ok, message: data.message, data };
}

async function logout() {
    await apiCall('/auth/logout', 'POST');
    sessionStorage.clear();
    window.location.href = 'index.html';
}

async function isAuthenticated() {
    const { ok } = await apiCall('/auth/me');
    return ok;
}

async function getCurrentUser() {
    const { ok, data } = await apiCall('/auth/me');
    if (!ok) return null;
    return data;
}

// ─── Quick sync reads from sessionStorage (no network needed) ─────────────────
function getUserType()      { return sessionStorage.getItem('userType'); }
function getUserName()      { return sessionStorage.getItem('userName'); }
function getCafeteriaId()   { return sessionStorage.getItem('cafeteriaId'); }
function getCafeteriaName() { return sessionStorage.getItem('cafeteriaName'); }

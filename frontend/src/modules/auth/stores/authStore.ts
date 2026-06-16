import { computed, reactive } from "vue";

import { fetchCurrentUser, login as loginApi, logout as logoutApi } from "../api/authApi";
import type { CurrentUser, LoginPayload, UserBrief } from "../types/auth";

const TOKEN_KEY = "stock_forum_token";
const USER_KEY = "stock_forum_user";

function readStoredUser(): CurrentUser | UserBrief | null {
  const raw = localStorage.getItem(USER_KEY);
  if (!raw) return null;
  try {
    return JSON.parse(raw) as CurrentUser | UserBrief;
  } catch {
    localStorage.removeItem(USER_KEY);
    return null;
  }
}

export const authState = reactive({
  token: localStorage.getItem(TOKEN_KEY),
  user: readStoredUser(),
  initialized: false,
  loading: false
});

export const isAuthenticated = computed(() => Boolean(authState.token));

export function hasAuthToken() {
  return Boolean(authState.token || localStorage.getItem(TOKEN_KEY));
}

export function saveAuth(token: string, user: CurrentUser | UserBrief) {
  authState.token = token;
  authState.user = user;
  localStorage.setItem(TOKEN_KEY, token);
  localStorage.setItem(USER_KEY, JSON.stringify(user));
}

export function clearAuth() {
  authState.token = null;
  authState.user = null;
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(USER_KEY);
}

export async function login(payload: LoginPayload) {
  const result = await loginApi(payload);
  saveAuth(result.token, result.user);
  return result.user;
}

export async function loadCurrentUser() {
  if (!hasAuthToken()) {
    authState.initialized = true;
    return null;
  }
  authState.loading = true;
  try {
    const user = await fetchCurrentUser();
    authState.user = user;
    localStorage.setItem(USER_KEY, JSON.stringify(user));
    return user;
  } catch {
    clearAuth();
    return null;
  } finally {
    authState.loading = false;
    authState.initialized = true;
  }
}

export async function logout() {
  try {
    if (hasAuthToken()) {
      await logoutApi();
    }
  } finally {
    clearAuth();
  }
}

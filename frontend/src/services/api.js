import axios from "axios";
import {
  clearTokens,
  getAccessToken,
  getRefreshToken,
  setAccessToken,
} from "../utils/auth";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  headers: { "Content-Type": "application/json" },
});

// Attach the JWT to every outgoing request, if we have one.
api.interceptors.request.use((config) => {
  const token = getAccessToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// --- Refresh-token handling ---
// If several requests 401 at once, only the first triggers a refresh call;
// the rest wait on this queue and retry once the new token lands.
let isRefreshing = false;
let pendingQueue = [];

// Bumped by invalidateSession() on logout. A refresh that was already in
// flight when logout happened checks this before writing a token back, so
// a stale refresh can't silently re-authenticate a user who just logged out.
let sessionEpoch = 0;

export function invalidateSession() {
  sessionEpoch += 1;
}

function flushQueue(error, token) {
  pendingQueue.forEach(({ resolve, reject }) => {
    if (error) reject(error);
    else resolve(token);
  });
  pendingQueue = [];
}

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    const status = error.response?.status;
    const isAuthEndpoint = originalRequest?.url?.includes("/auth/");

    if (status === 401 && !isAuthEndpoint && !originalRequest._retry) {
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          pendingQueue.push({ resolve, reject });
        }).then((token) => {
          originalRequest.headers.Authorization = `Bearer ${token}`;
          return api(originalRequest);
        });
      }

      originalRequest._retry = true;
      isRefreshing = true;
      const refreshToken = getRefreshToken();
      const epochAtStart = sessionEpoch;

      if (!refreshToken) {
        clearTokens();
        window.location.href = "/login";
        return Promise.reject(error);
      }

      try {
        const { data } = await axios.post(
          `${import.meta.env.VITE_API_BASE_URL}/api/v1/auth/refresh`,
          { refresh_token: refreshToken }
        );

        // A logout happened while this refresh was in flight — discard the
        // result instead of writing a fresh token back into a session the
        // user already ended.
        if (sessionEpoch !== epochAtStart) {
          flushQueue(error, null);
          return Promise.reject(error);
        }

        setAccessToken(data.access_token);
        flushQueue(null, data.access_token);
        originalRequest.headers.Authorization = `Bearer ${data.access_token}`;
        return api(originalRequest);
      } catch (refreshError) {
        flushQueue(refreshError, null);
        clearTokens();
        window.location.href = "/login";
        return Promise.reject(refreshError);
      } finally {
        isRefreshing = false;
      }
    }

    // Normalize the error message in one place (Section 3 contract: message / detail).
    let friendlyMessage = "Something went wrong. Please try again.";
    if (!error.response) {
      friendlyMessage =
        "Cannot reach the server. Check that the backend is running and VITE_API_BASE_URL is correct.";
    } else if (error.response.data?.message) {
      friendlyMessage = error.response.data.message;
    } else if (error.response.data?.detail) {
      const detail = error.response.data.detail;
      if (typeof detail === "string") {
        friendlyMessage = detail;
      } else if (Array.isArray(detail)) {
        friendlyMessage = detail
          .map((d) => (typeof d === "string" ? d : d.msg || `${d.loc ? d.loc.join(".") + ": " : ""}${d.msg || JSON.stringify(d)}`))
          .join("; ");
      }
    }
    return Promise.reject(Object.assign(error, { friendlyMessage }));
  }
);

export default api;
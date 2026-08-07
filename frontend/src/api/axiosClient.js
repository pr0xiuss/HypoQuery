import axios from "axios";

const axiosClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  headers: { "Content-Type": "application/json" },
});

// Attach the JWT to every request, if we have one.
axiosClient.interceptors.request.use((config) => {
  const token = localStorage.getItem("hypoquery_access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Normalize the error shape in one place.
// Backend contract (Section 4 addendum): { message, detail }.
// If this contract changes later, only this block needs updating.
axiosClient.interceptors.response.use(
  (response) => response,
  (error) => {
    const friendlyMessage =
      error.response?.data?.message ||
      error.response?.data?.detail ||
      "Something went wrong. Please try again.";
    return Promise.reject(Object.assign(error, { friendlyMessage }));
  }
);

export default axiosClient;

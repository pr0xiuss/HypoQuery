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
          .map((d) =>
            typeof d === "string"
              ? d
              : d.msg || `${d.loc ? d.loc.join(".") + ": " : ""}${d.msg || JSON.stringify(d)}`
          )
          .join("; ");
      }
    }
    return Promise.reject(Object.assign(error, { friendlyMessage }));
  }
);

export default axiosClient;

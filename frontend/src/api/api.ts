import axios from "axios";
import Cookies from "js-cookie";

const API_URL = import.meta.env.VITE_API_URL;

const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
    Accept: "application/json"
  },
  withCredentials: true,
});

// Interceptor – before sending the request
api.interceptors.request.use(
  (config) => {
    // For data update methods, add CSRF token
    const method = config.method?.toUpperCase();
    const modifyingMethods = ["POST", "PUT", "PATCH", "DELETE"];

    if (method && modifyingMethods.includes(method)) {
      const csrfToken = Cookies.get("csrf_access_token");
      if (csrfToken) {
        config.headers["X-CSRF-TOKEN"] = csrfToken;
      }
    }

    return config;
  },
  (error) => Promise.reject(error)
);

// INTERCEPTOR: Global error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

export default api;

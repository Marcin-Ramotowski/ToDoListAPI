import axios from "axios";
import Cookies from "js-cookie";

const API_URL = "http://localhost:5000";

const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
    Accept: "application/json",
    "X-CSRF-TOKEN": Cookies.get("csrf_access_token")
  },
  withCredentials: true,
});

export default api;

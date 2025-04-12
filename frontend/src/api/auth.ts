import axios from "axios";
import Cookies from "js-cookie";

const API_URL = "http://localhost:5000";

export const logout = async () => {
  try {
    await axios.get(`${API_URL}/logout`, { withCredentials: true });
  } catch (error) {
    console.error("Error during logout:", error);
  }

  // Remove JWT token from cookies
  document.cookie = "access_token_cookie=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
  localStorage.removeItem("user_id");
};

export const getCsrfToken = () => {
  const value = Cookies.get("csrf_access_token");
  const header = {"X-CSRF-TOKEN": value}
  return header;
};
import axios from "axios";
import Cookies from "js-cookie";

const API_URL = "http://localhost:5000";

const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
    Accept: "application/json",
  },
  withCredentials: true,
});

// User login
export const login = async (username: string, password: string) => {
  try {
    const response = await api.post("/login", { username, password });

    const userId = response.data.user_id;

    Cookies.set("user_id", String(userId), { secure: true, sameSite: "Strict" });

    return { userId };
  } catch (error) {
    throw new Error("Incorrect username or password.");
  }
};

// Get user tasks
export const getTasks = async () => {
  const userId = Cookies.get("user_id");
  if (!userId) throw new Error("No user_id in cookies.");

  const response = await api.get(`/tasks/user/${userId}`);
  return response.data;
};

// Logout
export const logout = async () => {
  await api.get("/logout"); // API usunie JWT
  Cookies.remove("access_token_cookie");
  Cookies.remove("user_id");
};

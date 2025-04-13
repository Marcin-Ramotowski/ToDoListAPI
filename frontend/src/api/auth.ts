import Cookies from "js-cookie";
import api from "./api";

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

// Logout
export const logout = async () => {
  await api.get("/logout"); // API removes JWT
  Cookies.remove("access_token_cookie");
  Cookies.remove("user_id");
};

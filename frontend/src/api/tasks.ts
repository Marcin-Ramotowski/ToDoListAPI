import axios from "axios";
import { getCsrfToken } from "./auth";

const API_URL = "http://localhost:5000";

// Get user tasks
export const getUserTasks = async (userId: number) => {
  const response = await axios.get(`${API_URL}/tasks/user/${userId}`, {withCredentials: true, headers: getCsrfToken()});
  return response.data;
};

// Create new task
export const createTask = async (taskData: {
  title: string;
  description: string;
  due_date: string;
  done: boolean;
}) => {
  const response = await axios.post(`${API_URL}/tasks`, taskData, {withCredentials: true, headers: getCsrfToken()});
  return response.data;
};

// Delete task
export const deleteTask = async (taskId: number) => {
  await axios.delete(`${API_URL}/tasks/${taskId}`, {withCredentials: true, headers: getCsrfToken()});
};

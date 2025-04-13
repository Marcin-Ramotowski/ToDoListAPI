import api from "./api"

// Get user tasks
export const getUserTasks = async (userId: number) => {
  const response = await api.get(`/tasks/user/${userId}`);
  return response.data;
};

// Create new task
export const createTask = async (taskData: {
  title: string;
  description: string;
  due_date: string;
  done: boolean;
}) => {
  const response = await api.post("/tasks", taskData);
  return response.data;
};

// Delete task
export const deleteTask = async (taskId: number) => {
  await api.delete(`/tasks/${taskId}`)
};

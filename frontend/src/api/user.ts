import api from "./api";

export const getUser = async (userId: number) => {
  const response = await api.get(`/users/${userId}`);
  return response.data;
};

export const updateUser = async (
  userId: number,
  data: {
    username: string;
    email: string;
    password?: string;
    oldPassword?: string;
  }
) => {
  const response = await api.patch(`/users/${userId}`, data);
  return response.data;
};

export const deleteUser = async (userId: number) => {
    const response = await api.delete(`/users/${userId}`);
    return response.data;
  };
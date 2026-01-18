import axios from "axios";
import { useAuthStore } from "../auth/auth.store";

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});

api.interceptors.request.use(
  (config) => {
    const token = useAuthStore.getState().token;

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => Promise.reject(error)
);

api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.data) {
      return Promise.reject(error.response.data);
    }

    return Promise.reject({
      success: false,
      error: {
        code: "FRONT_001",
        message: "Erro inesperado de comunicação",
      },
    });
  }
);

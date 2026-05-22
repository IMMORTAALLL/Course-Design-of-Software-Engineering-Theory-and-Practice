import axios from "axios";
import type { AxiosRequestConfig } from "axios";

export interface ApiResponse<T> {
  code: number;
  message: string;
  data: T;
}

export interface PageResult<T> {
  items: T[];
  page: number;
  size: number;
  total: number;
}

const request = axios.create({
  baseURL: "/api",
  timeout: 10000
});

request.interceptors.request.use((config) => {
  const token = localStorage.getItem("stock_forum_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

async function unwrap<T>(promise: Promise<{ data: ApiResponse<T> }>): Promise<T> {
  const response = await promise;
  const body = response.data;
  if (body.code !== 0) {
    if (body.code === 40101 || body.code === 40102) {
      localStorage.removeItem("stock_forum_token");
      localStorage.removeItem("stock_forum_user");
    }
    throw new Error(body.message || "请求失败");
  }
  return body.data;
}

export default {
  get<T>(url: string, config?: AxiosRequestConfig) {
    return unwrap<T>(request.get<ApiResponse<T>>(url, config));
  },
  post<T>(url: string, data?: unknown, config?: AxiosRequestConfig) {
    return unwrap<T>(request.post<ApiResponse<T>>(url, data, config));
  },
  put<T>(url: string, data?: unknown, config?: AxiosRequestConfig) {
    return unwrap<T>(request.put<ApiResponse<T>>(url, data, config));
  },
  delete<T>(url: string, config?: AxiosRequestConfig) {
    return unwrap<T>(request.delete<ApiResponse<T>>(url, config));
  }
};

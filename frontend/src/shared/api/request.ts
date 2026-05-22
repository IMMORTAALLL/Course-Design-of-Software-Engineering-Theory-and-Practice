import axios from "axios";

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

async function unwrap<T>(promise: Promise<{ data: ApiResponse<T> }>): Promise<T> {
  const response = await promise;
  const body = response.data;
  if (body.code !== 0) {
    throw new Error(body.message || "请求失败");
  }
  return body.data;
}

export default {
  get<T>(url: string, config?: Record<string, unknown>) {
    return unwrap<T>(request.get<ApiResponse<T>>(url, config));
  },
  post<T>(url: string, data?: unknown, config?: Record<string, unknown>) {
    return unwrap<T>(request.post<ApiResponse<T>>(url, data, config));
  },
  put<T>(url: string, data?: unknown, config?: Record<string, unknown>) {
    return unwrap<T>(request.put<ApiResponse<T>>(url, data, config));
  },
  delete<T>(url: string, config?: Record<string, unknown>) {
    return unwrap<T>(request.delete<ApiResponse<T>>(url, config));
  }
};

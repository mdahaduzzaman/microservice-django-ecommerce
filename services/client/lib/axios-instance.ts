import axios from "axios";
import { auth } from "@/auth";

const baseURL = process.env.NEXT_PUBLIC_API_URL;

// 1. Public Axios instance (no auth)
export const publicAxios = axios.create({
  baseURL,
});

// 2. Authorized Axios instance (with auth interceptor)
const authAxios = axios.create({
  baseURL,
});

// Add interceptor to authAxios only
authAxios.interceptors.request.use(
  async (config) => {
    const session = await auth();
    if (session?.access_token) {
      config.headers.Authorization = `Bearer ${session.access_token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default authAxios;

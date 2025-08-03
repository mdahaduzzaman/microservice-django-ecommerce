import axios from "axios";
import { auth } from "@/auth";

const axiosInstance = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
});

// For server-side usage (API routes, server components)
axiosInstance.interceptors.request.use(
  async (config) => {
    const session = await auth();
    console.log(session, "Session in axios interceptor");
    if (session?.access_token) {
      config.headers.Authorization = `Bearer ${session.access_token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default axiosInstance;
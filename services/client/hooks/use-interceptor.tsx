"use client";

import { publicAxios } from "@/lib/axios-instance";
import { useSession } from "next-auth/react";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

function useInterceptor() {
  const router = useRouter();
  const { data: session } = useSession();

  useEffect(() => {
    const requestInterceptor = publicAxios.interceptors.request.use(
      (config) => {
        if (session && !config.headers["Authorization"]) {
          config.headers["Authorization"] = `Bearer ${session?.access_token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    return () => {
      publicAxios.interceptors.request.eject(requestInterceptor);
    };
  }, [session, router]);

  return publicAxios;
}

export default useInterceptor;

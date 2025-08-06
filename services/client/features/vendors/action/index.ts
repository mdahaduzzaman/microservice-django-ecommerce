"use server";

import authAxios, { publicAxios } from "@/lib/axios-instance";
import { SubscriptionPlan } from "@/lib/types";

export const getSubscriptionPlans = async (): Promise<SubscriptionPlan[]> => {
  const response = await publicAxios.get("/api/v1/vendors/subscription-plans/");
  return response.data;
};

export const getVendor = async () => {
  const response = await authAxios.get("/api/v1/vendors/me/");

  return response.data;
};

export const createVendor = async (data: any) => {
  try {
    const response = await authAxios.post("/api/v1/vendors/me/", data);

    return response.data;
  } catch (error: any) {
    return {
      status: error.response.status,
      errors: error.response.data,
    };
  }
};

export const updateVendor = async (data: any) => {
  const response = await authAxios.put("/api/v1/vendors/me/", data);

  return response.data;
};

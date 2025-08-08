"use server";

import authAxios, { publicAxios } from "@/lib/axios-instance";
import { PaymentMethod } from "@/lib/types";

export const getPaymentMethods = async (): Promise<PaymentMethod[]> => {
  const response = await publicAxios.get("/api/v1/payments/payment-methods/");
  return response.data;
};

export const checkSession = async (data: any) => {
  const response = await authAxios.post(
    "/api/v1/payments/check-session/",
    data
  );

  return response.data;
};

"use server";

import { publicAxios } from "@/lib/axios-instance";
import { PaymentMethod } from "@/lib/types";

export const getPaymentMethods = async (): Promise<PaymentMethod[]> => {
  const response = await publicAxios.get("/api/v1/payments/payment-methods/");
  return response.data;
};

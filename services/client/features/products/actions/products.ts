import axiosInstance from "@/lib/axios-instance";
import { Product } from "@/types";

export const getProducts = async (params: any): Promise<Product[]> => {
  const response = await axiosInstance.get("/products", { params });
  return response.data;
};

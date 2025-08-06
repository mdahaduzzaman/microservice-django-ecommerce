import { publicAxios } from "@/lib/axios-instance";
import { Product } from "@/lib/types";

export const getProducts = async (params: any): Promise<Product[]> => {
  const response = await publicAxios.get("/catalog/products", { params });
  return response.data;
};

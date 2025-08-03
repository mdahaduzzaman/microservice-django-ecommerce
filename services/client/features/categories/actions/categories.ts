import axiosInstance from "@/lib/axios-instance";
import { Category } from "@/types";

export const getCategories = async (): Promise<Category[]> => {
  const response = await axiosInstance.get("/catalogs/categories/");

  return response.data;
};

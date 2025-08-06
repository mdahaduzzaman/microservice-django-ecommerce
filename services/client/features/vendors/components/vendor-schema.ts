import { z } from "zod";

export const vendorSchema = z.object({
  id: z.string().optional(),
  name: z.string().min(2).max(100),
  email: z.email(),
  phone: z.string().min(10).max(15),
  address: z.string().min(5).max(200),
  plan: z.string().min(2).max(100),
  billing_cycle: z.string().min(2),
});

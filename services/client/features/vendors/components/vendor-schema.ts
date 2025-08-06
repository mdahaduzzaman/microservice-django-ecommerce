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

export const vendorPaymentSchema = z.object({
  payment_method: z.string().min(1, {
    error: "Payment method is required",
  }),
  quantity: z.number(),
  plan: z.string().min(1),
  vendor: z.string().min(1),
  success_url: z.string().min(1),
  cancel_url: z.string().min(1),
});

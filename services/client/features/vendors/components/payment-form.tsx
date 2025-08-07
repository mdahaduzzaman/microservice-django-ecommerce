"use client";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Form,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import PaymentMethodsSelect from "@/features/payments/components/payment-methods-select";
import { PaymentMethod } from "@/lib/types";
import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation, useQuery } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { toast } from "sonner";
import { z } from "zod";
import {
  getSubscriptionPlan,
  getVendor,
  subscriptionCheckoutSession,
} from "../action";
import { vendorPaymentSchema } from "./vendor-schema";
import { Loader } from "lucide-react";

type Props = {
  plan: string;
  billingCycle: string;
  paymentMethods: PaymentMethod[];
};

type VendorPaymentSchema = z.infer<typeof vendorPaymentSchema>;

function PaymentForm({ plan, billingCycle, paymentMethods }: Props) {
  const [origin, setOrigin] = useState<string>("");
  const router = useRouter();

  const { data: vendor } = useQuery({
    queryKey: ["vendor"],
    queryFn: getVendor,
  });

  console.log("vendor", vendor);

  const { data: subscriptionPlan } = useQuery({
    queryKey: ["subscription-plans", plan],
    queryFn: () => getSubscriptionPlan(plan),
    enabled: !!plan,
  });

  console.log("subscriptionPlan", subscriptionPlan);

  const form = useForm<VendorPaymentSchema>({
    resolver: zodResolver(vendorPaymentSchema),
    defaultValues: {
      payment_method: "",
      quantity: billingCycle === "monthly" ? 1 : 12,
      plan: plan,
      vendor: "",
    },
  });

  const handleErrors = (errors: any) => {
    Object.entries(errors).forEach(([key, value]) => {
      form.setError(key as keyof VendorPaymentSchema, {
        type: "manual",
        message: (value as string[])[0].replace("Vendor", "Seller"),
      });
    });
  };

  const mutation = useMutation({
    mutationFn: subscriptionCheckoutSession,
    onSuccess: (data) => {
      console.log("data", data);
      if (data.errors) {
        handleErrors(data.errors);
        toast.error("Failed to checkout");
        return;
      }
      toast.success("Redirecting to payment gateway...");
      router.push(data.checkout_url);
    },
  });

  useEffect(() => {
    if (subscriptionPlan && vendor) {
      form.reset({
        ...form.getValues(),
        payment_method: "",
        quantity: billingCycle === "monthly" ? 1 : 12,
        plan: subscriptionPlan.id,
        vendor: vendor.id,
        success_url: `${origin}/vendor/onboarding/payments/status`,
        cancel_url: `${origin}/vendor/onboarding/payments/status`,
      });
    }
  }, [subscriptionPlan, vendor]);

  useEffect(() => {
    if (typeof window !== "undefined") {
      setOrigin(window.location.origin);
    }
  }, []);

  function onSubmit(data: VendorPaymentSchema) {
    console.log("data", data);
    mutation.mutate(data);
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        <div
          className={`rounded-2xl border shadow-md p-6 transition-all duration-200 ${
            subscriptionPlan?.is_popular
              ? "border-blue-500 shadow-blue-200"
              : "border-gray-200"
          }`}
        >
          {subscriptionPlan?.is_popular && (
            <div className="text-sm font-semibold text-blue-600 mb-2">
              Most Popular
            </div>
          )}
          <div className="flex items-center justify-between mb-2">
            <h2 className="text-xl font-bold capitalize">
              {subscriptionPlan?.name} Plan
            </h2>
            <Badge>{billingCycle}</Badge>
          </div>
          <p className="text-gray-600 mt-1 mb-4">
            {subscriptionPlan?.description}
          </p>

          <div className="space-y-1 text-sm text-gray-700 mb-4">
            {subscriptionPlan?.features.map((feature, index) => (
              <div key={index} className="flex items-center gap-2">
                <span className="text-green-600">✓</span>
                <span>{feature}</span>
              </div>
            ))}
          </div>
          <hr className="border-gray-200" />

          <div className="rounded-2xl mt-2">
            {/* Payment Summary */}
            <div className="flex justify-between items-center">
              <p className="text-sm text-gray-500">Total Payment</p>
              <p className="text-lg font-semibold text-gray-800">
                $&nbsp;
                {billingCycle === "monthly"
                  ? subscriptionPlan?.monthly_price?.toFixed(2)
                  : (Number(subscriptionPlan?.yearly_price || 0) * 12).toFixed(
                      2
                    )}
              </p>
            </div>
          </div>
        </div>
        <FormField
          control={form.control}
          name="payment_method"
          render={({ field }) => (
            <FormItem className="w-full">
              <FormLabel>Payment Method</FormLabel>
              <PaymentMethodsSelect
                paymentMethods={paymentMethods}
                onChange={field.onChange}
                value={field.value}
                insideForm
              />
              <FormDescription>This is the payment method.</FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />

        <Button type="submit" disabled={mutation.isPending}>
          {mutation.isPending && <Loader className="animate-spin" />} Proceed to
          Checkout
        </Button>
      </form>
    </Form>
  );
}

export default PaymentForm;

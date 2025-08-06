"use client";

import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { getQueryClient } from "@/hooks/get-query-client";
import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation, useQuery } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { toast } from "sonner";
import { z } from "zod";
import { createVendor, getVendor, updateVendor } from "../action";
import { vendorSchema } from "./vendor-schema";

type Props = {
  plan: string;
  billingCycle: string;
};

function VendorForm({ plan, billingCycle }: Props) {
  const router = useRouter();
  const queryClient = getQueryClient();
  const { data: existingVendor } = useQuery({
    queryKey: ["vendor"],
    queryFn: getVendor,
  });

  const form = useForm<z.infer<typeof vendorSchema>>({
    resolver: zodResolver(vendorSchema),
    defaultValues: {
      name: "",
      email: "",
      phone: "",
      address: "",
      plan: plan,
      billing_cycle: billingCycle,
    },
  });

  const handleErrors = (errors: any) => {
    Object.entries(errors).forEach(([key, value]) => {
      form.setError(key as keyof z.infer<typeof vendorSchema>, {
        type: "manual",
        message: (value as string[])[0].replace("Vendor", "Seller"),
      });
    });
  };

  const mutation = useMutation({
    mutationFn: createVendor,
    onSuccess: (data) => {
      console.log("data", data);
      if (data.errors) {
        handleErrors(data.errors);
        toast.error("Failed to create seller profile");
        return;
      }
      toast.success("Vendor profile created successfully");
      queryClient.invalidateQueries({ queryKey: ["vendor"] });
      router.push(`/vendor/onboarding/${plan}/${billingCycle}/payment`);
    },
    onError: (error) => {
      console.log("error", error);
      toast.error("Failed to create seller profile");
    },
  });

  const updateMutation = useMutation({
    mutationFn: updateVendor,
    onSuccess: (data) => {
      console.log("data", data);
      if (data.errors) {
        handleErrors(data.errors);
        toast.error("Failed to update seller profile");
        return;
      }
      toast.success("Vendor profile updated successfully");
      queryClient.invalidateQueries({ queryKey: ["vendor"] });
    },
    onError: (error) => {
      console.error("Error updating seller profile:", error);
      toast.error("Failed to update seller profile");
    },
  });

  useEffect(() => {
    if (existingVendor) {
      form.reset({
        name: existingVendor.name,
        email: existingVendor.email,
        phone: existingVendor.phone,
        address: existingVendor.address,
        plan: existingVendor.plan,
        billing_cycle: existingVendor.billing_cycle,
      });
    }
  }, [existingVendor]);

  function onSubmit(data: z.infer<typeof vendorSchema>) {
    if (existingVendor) {
      updateMutation.mutate(data);
    } else {
      mutation.mutate(data);
    }
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        <FormField
          control={form.control}
          name="name"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Shop Name</FormLabel>
              <FormControl>
                <Input placeholder="Shop Sphere" {...field} />
              </FormControl>
              <FormDescription>This is your shop name.</FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Shop Email</FormLabel>
              <FormControl>
                <Input placeholder="shop@example.com" {...field} />
              </FormControl>
              <FormDescription>This is your shop email.</FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="phone"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Shop Phone</FormLabel>
              <FormControl>
                <Input placeholder="(123) 456-7890" {...field} />
              </FormControl>
              <FormDescription>This is your shop phone number.</FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="address"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Shop Address</FormLabel>
              <FormControl>
                <Textarea placeholder="123 Main St, Anytown, USA" {...field} />
              </FormControl>
              <FormDescription>This is your shop address.</FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit">Proceed Next</Button>
      </form>
    </Form>
  );
}

export default VendorForm;

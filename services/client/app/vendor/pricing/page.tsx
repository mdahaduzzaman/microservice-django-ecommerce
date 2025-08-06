import { getSubscriptionPlans } from "@/features/vendors/action";
import PricingTable from "@/features/vendors/components/pricing-table";
import { Metadata } from "next";
import { Suspense } from "react";

export const metadata: Metadata = {
  title: "Vendor Pricing | ShopSphere",
  description: "Pricing plans for vendors on ShopSphere",
};

export default function Page() {
  const planPromise = getSubscriptionPlans();
  return (
    <div className="container py-20">
      <div className="mb-12 space-y-4 text-center">
        <h2 className="text-4xl font-bold tracking-tight sm:text-5xl">
          Simple, transparent pricing for all.
        </h2>
        <p className="text-muted-foreground text-lg whitespace-pre-line">
          Choose the plan that works for you. <br />
          All plans include access to our platform, lead generation tools, and
          dedicated support.
        </p>
      </div>

      <Suspense fallback={<div className="text-center">Loading plans...</div>}>
        <PricingTable planPromise={planPromise} />
      </Suspense>
    </div>
  );
}

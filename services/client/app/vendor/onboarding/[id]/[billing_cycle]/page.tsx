import withAuth from "@/components/shared/with-auth";
import VendorForm from "@/features/vendors/components/vendor-form";
import { Metadata } from "next";

export const metadata: Metadata = {
  title: "Seller Registration | ShopSphere",
  description: "Become a seller on ShopSphere and reach customers worldwide",
};

async function page({
  params,
}: {
  params: Promise<{ id: string; billing_cycle: string }>;
}) {
  const { id, billing_cycle } = await params;

  return (
    <div className="w-2/3 mx-auto p-5 rounded-xl bg-secondary">
      <h1 className="text-3xl font-bold text-center mb-5">Seller Onboarding</h1>
      <VendorForm plan={id} billingCycle={billing_cycle} />
    </div>
  );
}

export default withAuth(page);

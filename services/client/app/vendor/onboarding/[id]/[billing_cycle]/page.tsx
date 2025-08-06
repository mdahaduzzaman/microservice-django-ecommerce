import withAuth from "@/components/shared/with-auth";
import VendorForm from "@/features/vendors/components/vendor-form";
import VendorTimeline from "@/features/vendors/components/vendor-timeline";
import { Metadata } from "next";

export const metadata: Metadata = {
  title: "Seller Registration | ShopSphere",
  description: "Become a seller on ShopSphere and reach customers worldwide",
};

const items = [
  {
    id: 1,
    date: "Mar 15, 2024",
    title: "User SignUp",
    description: "Initial team meeting.",
  },
  {
    id: 2,
    date: "Mar 22, 2024",
    title: "Vendor Onboarding",
    description: "Completed wireframes.",
  },
  {
    id: 3,
    date: "Apr 5, 2024",
    title: "Make Payment",
    description: "Backend development.",
  },
];

async function page({
  params,
}: {
  params: Promise<{ id: string; billing_cycle: string }>;
}) {
  const { id, billing_cycle } = await params;

  return (
    <div className="flex items-center py-10">
      <div className="mx-auto">
        <VendorTimeline items={items} />
      </div>
      <div className="w-2/3 mx-auto p-5 rounded-xl bg-secondary">
        <h1 className="text-3xl font-bold text-center mb-5">Seller Onboarding</h1>
        <VendorForm plan={id} billingCycle={billing_cycle} />
      </div>
    </div>
  );
}

export default withAuth(page);

import VendorTimeline from "@/features/vendors/components/vendor-timeline";
import React from "react";

const items = [
  {
    id: 1,
    date: "Mar 15, 2024",
    title: "User SignUp",
    description: "Initial team meeting.",
    url: "",
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

async function layout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex items-center py-10">
      <div className="mx-auto">
        <VendorTimeline items={items} />
      </div>
      {children}
    </div>
  );
}

export default layout;

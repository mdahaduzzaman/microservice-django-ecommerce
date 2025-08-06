"use client";

import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { useMediaQuery } from "@/hooks/use-media-query";
import confetti from "canvas-confetti";
import { use, useRef, useState } from "react";
import { SubscriptionPlan } from "@/lib/types";
import Plan from "./plan";

// const plans = [
//   {
//     name: "STARTER",
//     price: "10",
//     yearlyPrice: "8",
//     period: "per month",
//     features: [
//       "Up to 20 products",
//       "Commission Fee 10% per sale",
//       "48-hour support response time",
//       "Limited API access",
//       "Community support",
//     ],
//     description: "Perfect for individuals and small projects",
//     buttonText: "Get Starter",
//     href: "/vendor/onboarding?plan=starter",
//     isPopular: false,
//   },
//   {
//     name: "GROWTH",
//     price: "30",
//     yearlyPrice: "24",
//     period: "per month",
//     features: [
//       "Up to 200 products",
//       "Commission Fee 5% per sale",
//       "Advanced analytics",
//       "24-hour support response time",
//       "Full API access",
//       "Priority support",
//       "Team collaboration",
//       "Custom integrations",
//     ],
//     description: "Ideal for growing teams and businesses",
//     buttonText: "Get Growth",
//     href: "/vendor/onboarding?plan=growth",
//     isPopular: true,
//   },
//   {
//     name: "PRO",
//     price: "90",
//     yearlyPrice: "72",
//     period: "per month",
//     features: [
//       "Unlimited products",
//       "Commission Fee 2% per sale",
//       "Real-time analytics",
//       "Everything in Growth",
//       "Custom solutions",
//       "Dedicated account manager",
//       "1-hour support response time",
//       "Advanced security",
//       "Custom contracts",
//       "SLA agreement",
//     ],
//     description: "For large organizations with specific needs",
//     buttonText: "Get Pro",
//     href: "/vendor/onboarding?plan=pro",
//     isPopular: false,
//   },
// ];

type Props = {
  planPromise: Promise<SubscriptionPlan[]>;
};
function PricingTable({ planPromise }: Props) {
  const [isMonthly, setIsMonthly] = useState(true);
  const isDesktop = useMediaQuery("(min-width: 768px)");
  const switchRef = useRef<HTMLButtonElement>(null);
  const plans = use(planPromise);

  const handleToggle = (checked: boolean) => {
    setIsMonthly(!checked);
    if (checked && switchRef.current) {
      const rect = switchRef.current.getBoundingClientRect();
      const x = rect.left + rect.width / 2;
      const y = rect.top + rect.height / 2;

      confetti({
        particleCount: 50,
        spread: 60,
        origin: {
          x: x / window.innerWidth,
          y: y / window.innerHeight,
        },
        colors: [
          "hsl(var(--primary))",
          "hsl(var(--accent))",
          "hsl(var(--secondary))",
          "hsl(var(--muted))",
        ],
        ticks: 200,
        gravity: 1.2,
        decay: 0.94,
        startVelocity: 30,
        shapes: ["circle"],
      });
    }
  };
  return (
    <>
      <div className="mb-10 flex justify-center">
        <label className="relative inline-flex cursor-pointer items-center">
          <Label>
            <Switch
              ref={switchRef as any}
              checked={!isMonthly}
              onCheckedChange={handleToggle}
              className="relative"
            />
          </Label>
        </label>
        <span className="ml-2 font-semibold">
          Annual billing <span className="text-primary">(Save 20%)</span>
        </span>
      </div>

      <div className="sm:2 grid grid-cols-1 gap-4 md:grid-cols-3">
        {plans.map((plan, index) => (
          <Plan
            key={index}
            index={index}
            plan={plan}
            isDesktop={isDesktop}
            isMonthly={isMonthly}
          />
        ))}
      </div>
    </>
  );
}

export default PricingTable;

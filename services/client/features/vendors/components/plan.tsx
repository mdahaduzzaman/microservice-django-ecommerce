import { Button } from "@/components/ui/button";
import { SubscriptionPlan } from "@/lib/types";
import { cn } from "@/lib/utils";
import NumberFlow from "@number-flow/react";
import { motion } from "framer-motion";
import { Check, Star } from "lucide-react";
import { signIn } from "next-auth/react";

type Props = {
  plan: SubscriptionPlan;
  index: number;
  isMonthly: boolean;
  isDesktop: boolean;
};

function Plan({ plan, index, isMonthly, isDesktop }: Props) {
  return (
    <motion.div
      initial={{ y: 50, opacity: 1 }}
      whileInView={
        isDesktop
          ? {
              y: plan.is_popular ? -20 : 0,
              opacity: 1,
              x: index === 2 ? -30 : index === 0 ? 30 : 0,
              scale: index === 0 || index === 2 ? 0.94 : 1.0,
            }
          : {}
      }
      viewport={{ once: true }}
      transition={{
        duration: 1.6,
        type: "spring",
        stiffness: 100,
        damping: 30,
        delay: 0.4,
        opacity: { duration: 0.5 },
      }}
      className={cn(
        `bg-background relative rounded-2xl border-[1px] p-6 text-center lg:flex lg:flex-col lg:justify-center`,
        plan.is_popular ? "border-primary border-2" : "border-border",
        "flex flex-col",
        !plan.is_popular && "mt-5",
        index === 0 || index === 2
          ? "z-0 translate-x-0 translate-y-0 -translate-z-[50px] rotate-y-[10deg] transform"
          : "z-10",
        index === 0 && "origin-right",
        index === 2 && "origin-left"
      )}
    >
      {plan.is_popular && (
        <div className="bg-primary absolute top-0 right-0 flex items-center rounded-tr-xl rounded-bl-xl px-2 py-0.5">
          <Star className="text-primary-foreground h-4 w-4 fill-current" />
          <span className="text-primary-foreground ml-1 font-sans font-semibold">
            Popular
          </span>
        </div>
      )}
      <div className="flex flex-1 flex-col">
        <p className="text-muted-foreground text-base font-semibold">
          {plan.name.toUpperCase()}
        </p>
        <div className="mt-6 flex items-center justify-center gap-x-2">
          <span className="text-foreground text-5xl font-bold tracking-tight">
            <NumberFlow
              value={
                isMonthly
                  ? Number(plan.monthly_price)
                  : Number(plan.yearly_price)
              }
              format={{
                style: "currency",
                currency: "USD",
                minimumFractionDigits: 0,
                maximumFractionDigits: 0,
              }}
              transformTiming={{
                duration: 500,
                easing: "ease-out",
              }}
              willChange
              className="font-variant-numeric: tabular-nums"
            />
          </span>
          <span className="text-muted-foreground text-sm leading-6 font-semibold tracking-wide">
            / per month
          </span>
        </div>

        <p className="text-muted-foreground text-xs leading-5">
          {isMonthly ? "billed monthly" : "billed annually"}
        </p>

        <ul className="mt-5 flex flex-col gap-2">
          {plan.features.map((feature, idx) => (
            <li key={idx} className="flex items-start gap-2">
              <Check className="text-primary mt-1 h-4 w-4 flex-shrink-0" />
              <span className="text-left">{feature}</span>
            </li>
          ))}
        </ul>

        <hr className="my-4 w-full" />

        <Button
          onClick={() =>
            signIn("keycloak", {
              redirectTo:
                `${plan.href}/${plan.id}/${isMonthly ? "monthly" : "yearly"}`,
            })
          }
          variant={plan.is_popular ? "default" : "outline"}
          className="text-lg font-semibold tracking-tighter hover:bg-primary hover:text-primary-foreground hover:ring-primary transform-gpu ring-offset-current transition-all duration-300 ease-out hover:ring-2 hover:ring-offset-1"
        >
          {plan.button_text}
        </Button>
        <p className="text-muted-foreground mt-6 text-xs leading-5">
          {plan.description}
        </p>
      </div>
    </motion.div>
  );
}

export default Plan;

import withAuth from "@/components/shared/with-auth";
import { getPaymentMethods } from "@/features/payments/actions";
import PaymentForm from "@/features/vendors/components/payment-form";
import { PaymentMethod } from "@/lib/types";

async function page({
  params,
}: {
  params: Promise<{ plan: string; billing_cycle: string }>;
}) {
  const { plan, billing_cycle } = await params;

  const paymentMethods: PaymentMethod[] = await getPaymentMethods();

  return (
    <div className="w-2/3 mx-auto p-5 rounded-xl bg-secondary">
      <h1 className="text-3xl font-bold text-center mb-5">Make Payment</h1>
      <PaymentForm
        plan={plan}
        billingCycle={billing_cycle}
        paymentMethods={paymentMethods}
      />
    </div>
  );
}

export default withAuth(page);

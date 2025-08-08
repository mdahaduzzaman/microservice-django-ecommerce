import PaymentCard from "@/components/shared/payment-card";
import withAuth from "@/components/shared/with-auth";
import { checkSession } from "@/features/payments/actions";
import { getVendor } from "@/features/vendors/action";
import { XCircle } from "lucide-react";

type Props = {
  searchParams: {
    session_id: string;
  };
};

const success = {
  status: "success",
  title: "Payment Successful",
  description:
    "Thank you for your subscription! You're now allowed to customize your shops and add products.",
  amount: 0,
  payment_method: "Card",
  button_text: "Back to Dashboard",
  button_link:
    "/vendor/onboarding/d100c611-f836-4771-be2e-07b722595a3f/monthly/payment/status?session_id=123456",
};

const error = {
  status: "error",
  title: "Payment Failed",
  description: "There was an issue processing your payment. Please try again.",
  amount: 0,
  payment_method: "Card",
  button_text: "Back to Payment",
  button_link:
    "/vendor/onboarding/d100c611-f836-4771-be2e-07b722595a3f/monthly/payment/status?session_id=123456",
};

async function page({ searchParams }: Props) {
  const { session_id } = await searchParams;

  if (!session_id) {
    return (
      <div className="w-2/3 mx-auto p-5 mt-20 rounded-xl bg-destructive/10 text-destructive text-center">
        <XCircle className="mx-auto h-12 w-12" />
        <p className="text-xl mt-2 font-semibold">Missing session ID</p>
      </div>
    );
  }

  let sessionData = null;
  try {
    sessionData = await checkSession({ session_id });
  } catch (error: any) {
    console.error("Error fetching session data:", error.response.data);
  }

  if (!sessionData) {
    return (
      <div className="w-2/3 mx-auto p-5 mt-20 rounded-xl bg-destructive/10 text-destructive text-center">
        <XCircle className="mx-auto h-12 w-12" />
        <p className="text-xl mt-2 font-semibold">Invalid session ID</p>
      </div>
    );
  }

  const vendor = await getVendor()

  const isSuccess = sessionData.payment_status === "paid";

  const updatedData = {
    ...(isSuccess ? success : error),
    amount: sessionData.amount_total,
    button_link: isSuccess ? success.button_link : `/vendor/onboarding/${vendor.plan}/${vendor.billing_cycle}/payment`
  };

  return (
    <div className="w-2/3 mx-auto p-5 rounded-xl bg-secondary flex justify-center items-center">
      <PaymentCard {...updatedData} />
    </div>
  );
}

export default withAuth(page);

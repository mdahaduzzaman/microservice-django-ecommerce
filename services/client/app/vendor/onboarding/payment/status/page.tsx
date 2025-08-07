import PaymentCard from "@/components/shared/payment-card";
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
  amount: 1000,
  payment_method: "Credit Card",
  button_text: "Back to Dashboard",
  button_link:
    "/vendor/onboarding/d100c611-f836-4771-be2e-07b722595a3f/monthly/payment/status?session_id=123456",
};

const error = {
  status: "error",
  title: "Payment Failed",
  description: "There was an issue processing your payment.",
  amount: 1000,
  payment_method: "Credit Card",
  button_text: "Back to Dashboard",
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

  const isSuccess = false;

  const updatedData = {
    ...(isSuccess ? success : error),
    status: isSuccess ? "success" : "error",
    title: isSuccess ? "Payment Successful" : "Payment Failed",
  };

  return (
    <div className="w-2/3 mx-auto p-5 rounded-xl bg-secondary flex justify-center items-center">
      <PaymentCard {...updatedData} />
    </div>
  );
}

export default page;

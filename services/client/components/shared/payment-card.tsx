import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import Image from "next/image";
import Link from "next/link";
import { Separator } from "../ui/separator";

type Props = {
  status: string;
  title: string;
  description: string;
  amount: number;
  payment_method: string;
  button_text: string;
  button_link: string;
};

function PaymentCard(props: Props) {
  return (
    <Card className="w-full max-w-sm">
      <CardHeader>
        <CardTitle className="flex flex-col items-center text-center">
          {props.status === "success" ? (
            <Image
              src={"/success.gif"}
              alt="Payment Successful"
              height={50}
              width={50}
            />
          ) : (
            <Image
              src={"/failed.gif"}
              alt="Payment Failed"
              height={50}
              width={50}
            />
          )}
          <h1 className="text-3xl text-center text-black font-bold mt-5 mb-3">
            {props.title}
          </h1>
        </CardTitle>
        <CardDescription>{props.description}</CardDescription>
      </CardHeader>
      <CardContent>
        <Separator />
        <div className="flex flex-col gap-2 py-2">
          <div className="flex items-center justify-between">
            <Label>Amount</Label>
            <span className="text-lg font-semibold">${props.amount / 100}</span>
          </div>
          <div className="flex items-center justify-between">
            <Label>Payment Method</Label>
            <span>{props.payment_method}</span>
          </div>
        </div>
        <Separator />
      </CardContent>
      <CardFooter className="flex-col gap-2">
        <Button asChild className="w-full">
          <Link href={props.button_link}>{props.button_text}</Link>
        </Button>
      </CardFooter>
    </Card>
  );
}

export default PaymentCard;

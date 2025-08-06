"use client";

import { FormControl } from "@/components/ui/form";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { PaymentMethod } from "@/lib/types";
import Image from "next/image";

type Props = {
  paymentMethods: PaymentMethod[];
  insideForm?: boolean;
  onChange?: (value: string) => void;
  value?: string;
};

function PaymentMethodsSelect({
  paymentMethods,
  insideForm,
  onChange,
  value,
}: Props) {
  return (
    <Select onValueChange={onChange} value={value}>
      {insideForm ? (
        <FormControl className="w-full">
          <SelectTrigger>
            <SelectValue placeholder="Select Payment Method" />
          </SelectTrigger>
        </FormControl>
      ) : (
        <SelectTrigger className="w-full">
          <SelectValue placeholder="Select Payment Method" />
        </SelectTrigger>
      )}
      <SelectContent>
        {paymentMethods.map((method) => (
          <SelectItem
            key={method.id}
            value={method.id}
            className="flex items-center gap-5"
          >
            <Image
              src={method.image_url}
              alt={method.name}
              width={24}
              height={24}
            />
            <span className="capitalize">{method.name}</span>
          </SelectItem>
        ))}
      </SelectContent>
    </Select>
  );
}

export default PaymentMethodsSelect;

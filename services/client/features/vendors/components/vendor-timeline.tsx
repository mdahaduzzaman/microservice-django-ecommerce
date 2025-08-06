"use client";

import {
  Timeline,
  TimelineHeader,
  TimelineIndicator,
  TimelineItem,
  TimelineSeparator,
  TimelineTitle,
} from "@/components/ui/timeline";
import { CheckIcon } from "lucide-react";
import { usePathname } from "next/navigation";

type Item = {
  id: number;
  date: string;
  title: string;
  description: string;
};

type Props = {
  items: Item[];
};

export default function VendorTimeline({ items }: Props) {
  const pathName = usePathname();
  const isPaymentPage = pathName.endsWith("/payment");
  const currentPage = isPaymentPage ? 2 : 1;

  return (
    <Timeline value={currentPage}>
      {items.map((item) => (
        <TimelineItem
          key={item.id}
          step={item.id}
          className="group-data-[orientation=vertical]/timeline:ms-10"
        >
          <TimelineHeader>
            <TimelineSeparator className="group-data-[orientation=vertical]/timeline:-left-7 group-data-[orientation=vertical]/timeline:h-[calc(100%-1.5rem-0.25rem)] group-data-[orientation=vertical]/timeline:translate-y-6.5" />
            <TimelineTitle className="-mt-0.5">{item.title}</TimelineTitle>
            <TimelineIndicator className="bg-primary/10 group-data-completed/timeline-item:bg-primary group-data-completed/timeline-item:text-primary-foreground flex size-6 items-center justify-center border-none group-data-[orientation=vertical]/timeline:-left-7">
              <CheckIcon
                className="group-not-data-completed/timeline-item:hidden"
                size={16}
              />
            </TimelineIndicator>
          </TimelineHeader>
        </TimelineItem>
      ))}
    </Timeline>
  );
}

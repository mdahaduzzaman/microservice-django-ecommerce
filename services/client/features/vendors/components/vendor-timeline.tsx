import {
  Timeline,
  TimelineHeader,
  TimelineIndicator,
  TimelineItem,
  TimelineSeparator,
  TimelineTitle,
} from "@/components/ui/timeline";

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
  return (
    <Timeline defaultValue={2}>
      {items.map((item) => (
        <TimelineItem key={item.id} step={item.id}>
          <TimelineHeader>
            <TimelineSeparator />
            <TimelineTitle className="-mt-0.5">{item.title}</TimelineTitle>
            <TimelineIndicator />
          </TimelineHeader>
        </TimelineItem>
      ))}
    </Timeline>
  );
}

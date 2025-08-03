"use client";

import { Card, CardContent } from "@/components/ui/card";
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
  type CarouselApi,
} from "@/components/ui/carousel";
import { cn } from "@/lib/utils";
import Autoplay from "embla-carousel-autoplay";
import * as React from "react";
import ItemOne from "./item-one";
import ItemTwo from "./item-two";
import ItemFive from "./item-five";
import ItemThree from "./item-three";
import ItemFour from "./item-four";

function HomeCarousel() {
  const [api, setApi] = React.useState<CarouselApi>();
  const [current, setCurrent] = React.useState(0);
  const [count, setCount] = React.useState(0);

  React.useEffect(() => {
    if (!api) {
      return;
    }

    setCount(api.scrollSnapList().length);
    setCurrent(api.selectedScrollSnap() + 1);

    api.on("select", () => {
      setCurrent(api.selectedScrollSnap() + 1);
    });
  }, [api]);
  return (
    <>
      <Carousel
        plugins={[
          Autoplay({
            delay: 5000,
          }),
        ]}
        setApi={setApi}
        className="h-full flex flex-col"
      >
        <CarouselContent className="h-[10rem] sm:h-[25rem] lg:h-[23rem]">
          <CarouselItem>
            <ItemOne />
          </CarouselItem>
          <CarouselItem>
            <ItemTwo />
          </CarouselItem>
          <CarouselItem>
            <ItemThree />
          </CarouselItem>
          <CarouselItem>
            <ItemFour />
          </CarouselItem>
          <CarouselItem>
            <ItemFive />
          </CarouselItem>
        </CarouselContent>
        <CarouselPrevious />
        <CarouselNext />
      </Carousel>
      <div className="absolute bottom-2 md:bottom-5 left-1/2 -translate-x-1/2 flex items-center justify-center gap-2">
        {Array.from({ length: count }).map((_, index) => (
          <button
            key={index}
            onClick={() => api?.scrollTo(index)}
            className={cn("size-2 md:size-3.5 rounded-full border md:border-2 border-black", {
              "border-red-500": current === index + 1,
            })}
          />
        ))}
      </div>
    </>
  );
}

export default HomeCarousel;

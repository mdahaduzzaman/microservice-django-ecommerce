import HomeCarousel from "@/components/customized/carousel/home-caousel";
import BecomeSeller from "@/components/shared/footer/become-seller";
import { Metadata } from "next";

export const metadata: Metadata = {
  title: "Online Shopping | ShopSphere",
  description: "Buy and sell products from all over the world",
};

export default async function Home() {
  return (
    <>
      <div className="flex flex-col md:flex-row gap-3 md:h-[75vh]">
        <div className="flex flex-col gap-3 w-full md:w-[75%]">
          <div className="h-[20vh] md:h-[70%] rounded-2xl relative overflow-hidden">
            <HomeCarousel />
          </div>
          <div className="flex flex-col md:flex-row gap-3 h-[30%]">
            <div className="w-full md:w-[40%] h-[7rem] md:h-auto bg-amber-500 rounded-2xl p-5">
              Box-1 Child-1
            </div>
            <div className="w-full md:w-[20%] h-[10rem] md:h-auto bg-cyan-500 rounded-2xl p-5">
              Box-1 Child-2
            </div>
            <div className="w-full md:w-[40%] h-[7rem] md:h-auto bg-orange-500 rounded-2xl p-5">
              Box-1 Child-3
            </div>
          </div>
        </div>
        <div className="flex flex-col gap-3 w-full md:w-[25%] rounded-2xl">
          <div className="bg-red-500 h-[7rem] md:h-[20%] p-5 rounded-2xl">
            Box-2 Child-1
          </div>
          <div className="bg-yellow-500 h-[10rem] md:h-[30%] p-5 rounded-2xl">
            Box-2 Child-2
          </div>
          <div className="bg-blue-500 h-[5rem] md:h-[50%] p-5 rounded-2xl">
            Box-2 Child-3
          </div>
        </div>
      </div>
      <BecomeSeller />
    </>
  );
}

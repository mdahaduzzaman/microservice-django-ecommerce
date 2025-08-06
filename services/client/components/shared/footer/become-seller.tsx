import { Button } from "@/components/ui/button";
import Link from "next/link";

const BecomeSeller = () => {
  return (
    <section className="my-3">
      <div className="">
        <div className="bg-accent flex w-full flex-col gap-16 overflow-hidden rounded-lg p-8 md:rounded-xl lg:flex-row lg:items-center lg:p-12">
          <div className="flex-1">
            <h3 className="mb-3 text-2xl font-semibold md:mb-4 md:text-4xl lg:mb-6">
              Become a Seller
            </h3>
            <p className="text-muted-foreground max-w-xl lg:text-lg">
              Join our platform as a seller and reach thousands of customers.
              Easily manage your products, track sales, and grow your business
              with powerful tools built just for you.
            </p>
          </div>
          <div className="flex shrink-0 flex-col gap-2 sm:flex-row">
            <Button variant="outline" asChild>
              <a href={"https://www.shadcnblocks.com"}>Learn More</a>
            </Button>

            <Button asChild variant="default">
              <Link href={"/vendor/pricing"}>Start Selling</Link>
            </Button>
          </div>
        </div>
      </div>
    </section>
  );
};

export default BecomeSeller;

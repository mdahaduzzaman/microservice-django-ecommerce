import { Separator } from "@/components/ui/separator";

function Footer() {
  return (
    <footer>
      <Separator />
      <div className="text-center py-4">
        @&nbsp;{new Date().getFullYear()}&nbsp;ShopSphere | All rights reserved.
      </div>
    </footer>
  );
}

export default Footer;

import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import React from "react";

function Footer() {
  return (
    <footer>
      <div>
        <Button>Become a Seller</Button>
      </div>
      <Separator />
      <div className="text-center py-4">
        @&nbsp;{new Date().getFullYear()}&nbsp;ShopSphere | All rights reserved.
      </div>
    </footer>
  );
}

export default Footer;

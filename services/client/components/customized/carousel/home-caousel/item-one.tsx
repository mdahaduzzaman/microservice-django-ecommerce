import { Button } from "@/components/ui/button";
import React from "react";

function ItemOne() {
  return (
    <div className=" bg-amber-100 w-full h-full  flex items-center justify-center">
      ItemOne
      <Button onClick={()=>alert("Button clicked!")}>Click Me</Button>
    </div>
  );
}

export default ItemOne;

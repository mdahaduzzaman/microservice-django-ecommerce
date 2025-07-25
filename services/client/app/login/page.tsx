import { auth } from "@/auth";
import SignIn from "@/components/sign-in";
import React from "react";

async function page() {
  const session = await auth();
  console.log(session);

  return (
    <div className="h-screen flex items-center justify-center">
      <SignIn />
    </div>
  );
}

export default page;

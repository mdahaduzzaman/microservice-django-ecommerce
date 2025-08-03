import { getSession } from "@/lib/get-session";
import { redirect } from "next/navigation";
import { ComponentType } from "react";

const withAuth = <P extends object>(Component: ComponentType<P>) => {
  const WithAuth = async (props: P) => {
    const session = await getSession();

    if (!session?.user) {
      redirect("/login");
    }

    return <Component {...props} />;
  };

  return WithAuth;
};

export default withAuth;

import { signIn } from "@/auth";
import { getSession } from "@/lib/get-session";
import { ComponentType } from "react";

const withAuth = <P extends object>(Component: ComponentType<P>) => {
  const WithAuth = async (props: P) => {
    const session = await getSession();
    if (session?.error === "RefreshTokenError") {
      await signIn("keycloak");
    }

    return <Component {...props} />;
  };

  return WithAuth;
};

export default withAuth;

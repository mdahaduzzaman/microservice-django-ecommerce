import { auth } from "@/auth";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Handbag, Heart, SearchSlash } from "lucide-react";
import { headers } from "next/headers";
import Link from "next/link";
import SignIn from "./sign-in";
import User from "./user";

const issuer_url = process.env.AUTH_KEYCLOAK_ISSUER;
const CLIENT_ID = process.env.AUTH_KEYCLOAK_ID;

export async function Header() {
  const session = await auth();
  const headersList = await headers();
  const host = await headersList.get("host");
  const protocol = headersList.get("x-forwarded-proto");
  const redirect_uri = `${protocol}://${host}/auth/signin`;

  const user = session?.user;

  const accountUrl = `${issuer_url}/account?referrer=${CLIENT_ID}&referrer=client&referrer_uri=${redirect_uri}`;

  return (
    <header className="z-20 sticky backdrop-blur-md top-5 mb-5 bg-gradient-to-r from-[#eaf5eb] to-[#f1f7f2] rounded-full shadow-md flex flex-col sm:flex-row items-center justify-between sm:p-2">
      <div className="flex items-center gap-5 md:px-5">
        <Link href={"/"} className="hidden sm:block">
          ShopSphere
        </Link>
        <div className="relative w-full md:min-w-[25vw]">
          <Input
            placeholder="Search products..."
            className="bg-white inset-0 rounded-full px-3 py-5 pr-12"
          />
          <Button
            size={"icon"}
            className="rounded-full absolute right-1 top-1/2 -translate-y-1/2"
          >
            <SearchSlash />
          </Button>
        </div>
      </div>
      <div className="hidden sm:flex items-center gap-1">
        <Button size={"icon"} variant={"outline"} className="rounded-full p-5">
          <Handbag />
        </Button>
        <Button size={"icon"} variant={"outline"} className="rounded-full p-5">
          <Heart className="text-red-500 fill-red-500" />
        </Button>

        {user ? (
          <User image={user.image} name={user.name} accountUrl={accountUrl} />
        ) : (
          <SignIn />
        )}
      </div>
    </header>
  );
}

export default Header;

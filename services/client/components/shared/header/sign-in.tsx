import { signIn } from "@/auth";
import { Button } from "@/components/ui/button";

export default function SignIn() {
  return (
    <form
      action={async () => {
        "use server";
        await signIn("keycloak");
      }}
    >
      <Button
        type="submit"
        size={"lg"}
        className="relative hover:cursor-pointer py-5 rounded-full flex items-center justify-between"
      >
        <span>Login</span>
      </Button>
    </form>
  );
}

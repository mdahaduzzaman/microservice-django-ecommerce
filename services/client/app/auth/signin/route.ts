import { signIn } from "@/auth";

export async function GET() {
  console.log("Executing signIn function");
  await signIn("keycloak");
}

import { signIn } from "@/auth";

export async function GET() {
  await signIn("keycloak");
}

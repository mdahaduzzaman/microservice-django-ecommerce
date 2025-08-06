import { signOut } from "@/auth";

export async function GET() {
  console.log("Executing signOut function");
  await signOut();
}

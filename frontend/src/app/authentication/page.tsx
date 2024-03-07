import { redirect } from "next/navigation";

export default function RedirectAuthenticationToLogin() {
  redirect("/authentication/login");
}

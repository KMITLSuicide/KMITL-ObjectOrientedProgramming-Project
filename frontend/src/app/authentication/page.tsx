"use client";

import { useRouter } from "next/navigation";

export default function RedirectAuthenticationToLogin() {
  const router = useRouter();
  router.push("/authentication/login");
  return(
    <>
      <h1>Redirecting...</h1>
    </>
  );
}
"use client";

import { toast } from "~/src/components/ui/use-toast";
import { Suspense, useEffect, useState } from "react";
import { Loader2 } from "lucide-react";
import { ToastAction } from "~/src/components/ui/toast";
import Link from "next/link";
import { getAccountDataFromAPI } from "~/src/lib/data/account/account";
import { type AccountInfo } from "~/src/lib/definitions/account";

export default function AccountPage() {
  const [accountData, setAccountData] = useState<
    AccountInfo | null | undefined
  >(undefined);

  useEffect(() => {
    async function fetchData() {
      const apiData = await getAccountDataFromAPI();
      setAccountData(apiData);
    }
    void fetchData();

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    if (accountData === null) {
      toast({
        title: "Failed to get account data",
        description: "Please log in to view your account data.",
        variant: "destructive",
        action: (
          <ToastAction altText="Log in" asChild>
            <Link href="/authentication/login">Log in</Link>
          </ToastAction>
        ),
      });
    }
    console.log(accountData);
  }, [accountData]);

  return (
    <div className="flex h-full w-full items-center justify-center">
      <div className="h-fit w-fit space-y-4 rounded-lg bg-secondary p-6">
        <h1 className="text-2xl font-extrabold">Your account</h1>
        <Suspense fallback={<Loader2 className="mr-2 h-4 w-4 animate-spin" />}>
          <table className="border-separate border-spacing-x-2">
            <tbody>
              <tr>
                <th className="text-end">Type</th>
                {accountData && (
                  <td>
                    {accountData.type === "user"
                      ? "Learner"
                      : accountData.type === "teacher"
                        ? "Teacher"
                        : null}
                  </td>
                )}
              </tr>
              <tr>
                <th className="text-end">ID</th>
                {accountData && <td>{accountData.id}</td>}
              </tr>
              <tr>
                <th className="text-end">Name</th>
                {accountData && <td>{accountData.name}</td>}
              </tr>
              <tr>
                <th className="text-end">Email</th>
                {accountData && <td>{accountData.email}</td>}
              </tr>
            </tbody>
          </table>
        </Suspense>
      </div>
    </div>
  );
}

'use client';

import api from "~/src/lib/data/api";
import { toast } from "~/src/components/ui/use-toast";
import { Suspense, useEffect, useState } from "react";
import { Loader2 } from "lucide-react";
import { Toaster } from "~/src/components/ui/toaster";
import { ToastAction } from "~/src/components/ui/toast";
import Link from "next/link";

interface AccountData {
  _User__id: string;
  _User__name: string;
  _User__email: string;
  _User__hashed_password: string;
  _User__my_progresses: any[];
  _User__latest_progress: null | any;
};

async function getAccountDataFromAPI() {
  try {
    const response = await api.get<AccountData>('/account');

    if (response.status == 200) {
      return response.data;
    } else {
      return null;
    }
  } catch (error) {
    console.error(error);
    return null;
  }
}

export default function AccountPage() {
  const [accountData, setAccountData] = useState<AccountData | null | undefined>(undefined);

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
        variant: 'destructive',
        action: <ToastAction altText="Log in" asChild>
          <Link href="/authentication/login">Log in</Link>
          </ToastAction>
      });
    }
    console.log(accountData); // Move the console.log statement here
  }, [accountData]);

  return(
  <div className="flex w-full h-full justify-center items-center">
    <div className="w-fit h-fit bg-secondary p-6 rounded-lg space-y-4">
      <h1 className="text-2xl font-extrabold">Your account</h1>
      <Suspense fallback={
        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
      }>
        <table className="border-separate border-spacing-x-2">
          <tbody>
            <tr>
              <th className="text-end">ID</th>
              {accountData && <td>{accountData._User__id}</td>}
            </tr>
            <tr>
              <th className="text-end">Name</th>
              {accountData && <td>{accountData._User__name}</td>}
            </tr>
            <tr>
              <th className="text-end">Email</th>
              {accountData && <td>{accountData._User__email}</td>}
            </tr>
            <tr>
              <th className="text-end">Hashed Password</th>
              {accountData && <td>{accountData._User__hashed_password}</td>}
            </tr>
          </tbody>
        </table>
      </Suspense>

      <Toaster />
    </div>
  </div>);
}
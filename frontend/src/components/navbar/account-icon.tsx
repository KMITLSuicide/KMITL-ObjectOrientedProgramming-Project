'use client';

import { UserRoundX, UserRoundCheck, UserRound } from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import Cookies from "js-cookie";
import {
  Avatar,
  AvatarFallback,
  AvatarImage,
} from "~/src/components/ui/avatar";
import { Button } from "~/src/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "~/src/components/ui/dropdown-menu";
import { getAccountDataFromAPI } from "~/src/lib/data/account/account";
import { logout } from "~/src/lib/data/authentication";
import { type AccountInfo } from "~/src/lib/definitions/account";

export default function AccountIcon() {
  const router = useRouter();
  const [accountData, setAccountData] = useState<AccountInfo | null>(null);
  const [token, setToken] = useState<string | null>(null);

  useEffect(() => {
    const token = Cookies.get('token');
    setToken(token ?? null);
  }, []);

  useEffect(() => {
    // eslint-disable-next-line @typescript-eslint/restrict-template-expressions
    console.log(`token: ${token}`);
    // console.log(`vanilla token: ${localStorage.getItem('token')}`)
  }, [token]);

  useEffect(() => {
    // eslint-disable-next-line @typescript-eslint/restrict-template-expressions
    console.log(`token: ${token}`);
    void getAccountDataFromAPI().then((data) => {
      setAccountData(data);
    });
    router.refresh();
  }, [router, token]);

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" className="relative h-8 w-8 rounded-full outline outline-1 outline-secondary">
          <Avatar className="h-8 w-8  items-center justify-center flex  ">
            <AvatarImage src="/default_avatar.png" asChild>
              {accountData ? (
                <UserRoundCheck className="m-[6px] dark:text-green-300 text-green-600" size={24} />
              ) : (
                <UserRoundX className="m-[6px] dark:text-red-300 text-red-600" size={24} />
              )}
            </AvatarImage>
            <AvatarFallback asChild>
              <UserRound className="m-[6px] bg-transparent" size={24} />
            </AvatarFallback>
          </Avatar>
        </Button>
      </DropdownMenuTrigger>
      {accountData ? (
        <DropdownMenuContent className="w-56" align="end" forceMount>
          <DropdownMenuLabel className="font-normal">
            <div className="flex flex-col space-y-1">
              <p className="text-sm font-medium leading-none">{accountData?.name ?? 'Name'}</p>
              <p className="text-xs leading-none text-muted-foreground">
                {accountData?.email ?? 'email@example.com'}
              </p>
            </div>
          </DropdownMenuLabel>
          <DropdownMenuSeparator />
          <DropdownMenuGroup>
            <DropdownMenuItem asChild>
              <Link href="/account">
                Profile
              </Link>
            </DropdownMenuItem>
            <DropdownMenuItem asChild>
              <Link href="/account/order">
                Orders
              </Link>
            </DropdownMenuItem>
          </DropdownMenuGroup>
          <DropdownMenuSeparator />
          <DropdownMenuItem onClick={() => {
            logout();
            setAccountData(null);
            router.refresh();
            router.push('/');
            }}>
            Log out
          </DropdownMenuItem>
        </DropdownMenuContent>
      ) : (
        <DropdownMenuContent className="w-56" align="end" forceMount>
          <DropdownMenuLabel className="font-normal">
            <p className="text-sm font-medium leading-none my-2">Not logged in.</p>
          </DropdownMenuLabel>
          <DropdownMenuSeparator />
          <DropdownMenuGroup>
            <DropdownMenuItem asChild>
              <Link href="/authentication/login">
                Log in
              </Link>
            </DropdownMenuItem>
            <DropdownMenuItem asChild>
              <Link href="/authentication/register">
                Register
              </Link>
            </DropdownMenuItem>
          </DropdownMenuGroup>
        </DropdownMenuContent>
      )}
    </DropdownMenu>
  );
}

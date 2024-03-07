'use client';

import { UserRoundX, UserRoundCheck } from "lucide-react";
import { useEffect, useState } from "react";
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
  DropdownMenuShortcut,
  DropdownMenuTrigger,
} from "~/src/components/ui/dropdown-menu";
import { getAccountDataFromAPI } from "~/src/lib/data/account";
import { type AccountInfo } from "~/src/lib/definitions/account";

export default function AccountIcon() {
  const [accountData, setAccountData] = useState<AccountInfo | null>(null);

  useEffect(() => {
    void getAccountDataFromAPI().then((data) => {
      setAccountData(data);
    });
  }, []);

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" className="relative h-8 w-8 rounded-full outline outline-1 outline-secondary">
          <Avatar className="h-8 w-8  items-center justify-center flex  ">
            <AvatarImage src="/default_avatar.png" asChild>
              {accountData ? (
                <UserRoundCheck color="#6ee7b7" className="h-6 w-6" size={24} />
              ) : (
                <UserRoundX color="#fca5a5" className="h-6 w-6" size={24} />
              )}
            </AvatarImage>
            <AvatarFallback>PY</AvatarFallback>
          </Avatar>
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent className="w-56" align="end" forceMount>
        <DropdownMenuLabel className="font-normal">
          <div className="flex flex-col space-y-1">
            <p className="text-sm font-medium leading-none">shadcn</p>
            <p className="text-xs leading-none text-muted-foreground">
              m@example.com
            </p>
          </div>
        </DropdownMenuLabel>
        <DropdownMenuSeparator />
        <DropdownMenuGroup>
          <DropdownMenuItem>
            Profile
            <DropdownMenuShortcut>⇧⌘P</DropdownMenuShortcut>
          </DropdownMenuItem>
          <DropdownMenuItem>
            Billing
            <DropdownMenuShortcut>⌘B</DropdownMenuShortcut>
          </DropdownMenuItem>
          <DropdownMenuItem>
            Settings
            <DropdownMenuShortcut>⌘S</DropdownMenuShortcut>
          </DropdownMenuItem>
          <DropdownMenuItem>New Team</DropdownMenuItem>
        </DropdownMenuGroup>
        <DropdownMenuSeparator />
        <DropdownMenuItem>
          Log out
          <DropdownMenuShortcut>⇧⌘Q</DropdownMenuShortcut>
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}

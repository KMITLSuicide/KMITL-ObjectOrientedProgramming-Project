import { cn } from "~/src/lib/utils";
import Logo from "~/src/components/navbar/logo";
import ThemeToggle from "~/src/components/navbar/theme-toggle";
import AccountIcon from "~/src/components/navbar/account-icon";
import { NavLinks, type NavItems } from "~/src/components/navbar/nav-links";
import { Search, ShoppingCart } from "lucide-react";
import { Button } from "~/src/components/ui/button";
import Link from "next/link";

const navItemsLeft: NavItems[] = [
  {
    href: "/category",
    label: "Categories",
  },
];

const navItemsRight: NavItems[] = [
  {
    href: "/account/teaching",
    label: "Teaching",
  },
  {
    href: "/account/learning",
    label: "Learning",
  },
];

export default function NavBar({
  className,
  ...props
}: React.HTMLAttributes<HTMLElement>) {
  return (
    <nav
      className={cn(
        "flex h-12 items-center space-x-4 border-b bg-background lg:space-x-6",
        className,
      )}
      {...props}
    >
      <Logo />
      <NavLinks items={navItemsLeft} />
      <Link href="/search">
        <Search size={20} className="text-muted-foreground hover:text-primary transition-colors" />
      </Link>

      <div className="flex-grow" />

      <NavLinks items={navItemsRight} />

      <Link href="/search">
        <ShoppingCart size={20} className="text-muted-foreground hover:text-primary transition-colors" />
      </Link>
      <ThemeToggle />
      <AccountIcon />
    </nav>
  );
}

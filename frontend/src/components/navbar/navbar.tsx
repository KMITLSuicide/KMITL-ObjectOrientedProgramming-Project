import { cn } from "~/src/lib/utils";
import Logo from "~/src/components/navbar/logo";
import ThemeToggle from "~/src/components/navbar/theme-toggle";
import Avatar from "~/src/components/navbar/avatar";
import NavLinks from "./nav-links";
import { Search } from "lucide-react";
import { Button } from "~/src/components/ui/button";
import Link from "next/link";

export default function NavBar({
    className,
    ...props
}: React.HTMLAttributes<HTMLElement>) {
    return (
        <nav
            className={cn(
                "flex items-center space-x-4 px-4 h-12 lg:space-x-6 bg-background border-b",
                className,
            )}
            {...props}
        >
            <Logo />
            <Button asChild variant="outline" size="icon">
                <Link href='/search'>
                    <Search className="h-[1.2rem] w-[1.2rem]" />
                </Link>
            </Button>

            <div className="flex-grow" />

            <NavLinks />

            <ThemeToggle />
            <Avatar />
        </nav>
    );
}

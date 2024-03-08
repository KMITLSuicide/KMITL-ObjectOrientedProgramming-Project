import Link from "next/link";

export interface NavItems {
  href: string;
  label: string;
}

export function NavLinks({
  items
} : {
  items: NavItems[]
}) {
  return (
    <>
      {items.map((item) => {
        return (
          <Link
            key={item.href}
            href={item.href}
            className="text-sm font-medium text-muted-foreground transition-colors hover:text-primary"
          >
            {item.label}
          </Link>
        );
      })}
    </>
  );
}

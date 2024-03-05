import Link from "next/link";

const links: {
  href: string;
  label: string;
}[] = [{
  href: "/category",
  label: "Categories",
}];


export default function NavLinks() {
  return (
    <>
      {links.map((link) => {
        return (
          <Link key={link.href} href={link.href} className="text-sm font-medium text-muted-foreground transition-colors hover:text-primary">
            {link.label}
          </Link>
        );
      })}
    </>
  );
}

import Image from "next/image";
import Link from "next/link";

export default function Logo() {
  return (
    <Link href={"/"}>
      <Image src="/logo.jpg" alt="logo" width={91} height={34} />
    </Link>
  );
}

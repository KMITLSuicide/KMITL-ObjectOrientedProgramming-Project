import Image from "next/image";

export default function Logo() {
    return(
        <>
            <Image src='/logo.jpg' alt="logo" width={91} height={34} />
        </>
    );
}
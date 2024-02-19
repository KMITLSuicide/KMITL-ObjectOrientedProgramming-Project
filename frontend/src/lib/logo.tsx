import Image from "next/image";

export default function Logo() {
    return(
        <>
            {/* <p>udemy</p> */}
            <Image src='/logo.jpg' alt="logo" width={182} height={68} />
        </>
    );
}
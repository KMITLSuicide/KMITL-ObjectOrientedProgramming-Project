import Image from "next/image";
import type { CourseLearnMaterialImage } from "~/src/lib/definitions/course";

export function CourseLearnImage({
  imageData,
}: {
  imageData: CourseLearnMaterialImage;
}) {
  return (
    <>
      {/* <div className="relative w-full max-h-[90%] h-full">
        <Image
          alt={imageData?.description ?? "description not found"}
          src={imageData?.url ?? "/notexture.png"}
          // width={1024}
          // height={1024}
          fill
          objectFit='contain'
          className="fixed mb-6 rounded-xl"
        />
      </div>
      <h1 className="my-8 text-3xl font-bold">{imageData?.name}</h1>
      <p>{imageData?.description}</p> */}
      <h1 className="text-2xl font-bold">Preview</h1>
      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img
        src={imageData?.url ?? "/notexture.png"}
        alt={imageData?.description ?? "description not found"}
        height={720}
        style={{
          objectFit: "contain",
          width: "100%",
          height: "720px",
        }}
      />
      <h2 className="text-2xl font-bold">{imageData?.name}</h2>
      <p>{imageData?.description}</p>
    </>
  );
}
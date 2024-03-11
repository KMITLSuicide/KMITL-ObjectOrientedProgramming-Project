import type { CourseLearnMaterialImage } from "~/src/lib/definitions/course";

export function CourseLearnImage({
  imageData,
}: {
  imageData: CourseLearnMaterialImage;
}) {
  return (
    <>
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
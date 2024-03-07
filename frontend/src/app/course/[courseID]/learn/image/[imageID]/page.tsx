"use client";

import Image from "next/image";
import { useEffect, useState } from "react";
import { getCourseLearnDataFromAPI } from "~/src/lib/data/course";
import { type CourseLearn } from "~/src/lib/definitions/course";

export default function CourseMaterialImage({
  params,
}: {
  params: { courseID: string; imageID: string };
}) {
  const [learnData, setLearnData] = useState<CourseLearn | null | undefined>(
    undefined,
  );
  useEffect(() => {
    void getCourseLearnDataFromAPI(params.courseID).then((data) => {
      setLearnData(data);
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const thisImage = learnData?.learn_materials_images.find(
    (image) => image.id === params.imageID,
  );

  return (
    <div className="space-y-2">
      <Image
        alt={thisImage?.description ?? "description not found"}
        src={thisImage?.url ?? "/notexture.png"}
        width={1024}
        height={1024}
        className="mb-6 rounded-xl"
      />
      <h1 className="my-8 text-3xl font-bold">{thisImage?.name}</h1>
      <p>{thisImage?.description}</p>
    </div>
  );
}

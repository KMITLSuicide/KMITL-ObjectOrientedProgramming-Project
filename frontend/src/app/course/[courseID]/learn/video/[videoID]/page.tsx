'use client';

import { useEffect, useState } from "react";
import { getCourseLearnDataFromAPI } from "~/src/lib/data/course";
import { type CourseLearn } from "~/src/lib/definitions/course";


export default function CourseMaterialImage({
  params,
}: {
  params: { courseID: string; videoID: string };
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

  const thisVideo = learnData?.learn_materials_videos.find(
    (video) => video.id === params.videoID,
  );

  return (
    <div className="space-y-2">
      <video width="1280" controls preload="none">
        <source src={thisVideo?.url}  />
        Your browser does not support the video tag.
      </video>
      <h1 className="text-3xl font-bold my-8">{thisVideo?.name}</h1>
      <p>{thisVideo?.description}</p>
    </div>
  );
}

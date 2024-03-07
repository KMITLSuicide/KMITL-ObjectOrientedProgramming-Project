"use client";

import React, { Suspense, useEffect, useState } from "react";
import { getCourseLearnDataFromAPI } from "~/src/lib/data/course";
import { type CourseLearn } from "~/src/lib/definitions/course";
import ReactPlayer from "react-player";
import { Skeleton } from "~/src/components/ui/skeleton";

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
    <div className="flex h-full flex-col space-y-2">
      {learnData && (
        <ReactPlayer
          url={thisVideo?.url}
          controls={true}
          width="100%"
          height="640px"
        />
      )}
      <h1 className="my-8 text-3xl font-bold">{thisVideo?.name}</h1>
      <p>{thisVideo?.description}</p>
    </div>
  );
}

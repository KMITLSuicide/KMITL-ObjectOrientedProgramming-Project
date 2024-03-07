'use client';

import { useEffect, useState } from "react";
import { getCourseLearnDataFromAPI } from "~/src/lib/data/course";
import { type CourseLearn } from "~/src/lib/definitions/course";

export default function CourseLearn({
  params,
}: {
  params: { courseID: string };
}) {
  const [learnData, setLearnData] = useState<CourseLearn | null | undefined>(undefined);
  useEffect(() => {
    void getCourseLearnDataFromAPI(params.courseID).then((data) => {
      setLearnData(data);
    });
  }, []);
  
  return (
    <div className="flex flex-col space-y-2">
      <h4 className="text-lg font-light">Learning</h4>
      <h1 className="text-4xl font-bold">{learnData?.name}</h1>
      <p className="text-lg">{learnData?.description}</p>
      <p className="text-base font-light">
        Please choose course material on the sidebar.
      </p>
    </div>
  );
}

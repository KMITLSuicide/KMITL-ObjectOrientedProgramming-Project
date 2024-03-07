'use client';

import { useEffect, useState } from "react";
import { getCourseLearnDataFromAPI } from "~/src/lib/data/course";
import { type CourseLearn } from "~/src/lib/definitions/course";


export default function CourseMaterialQuiz({
  params,
}: {
  params: { courseID: string; quizID: string };
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

  return (
    <>
      <h1>Course quiz</h1>
      <h2>id={params.courseID}</h2>
      <h2>id={params.quizID}</h2>
    </>
  );
}

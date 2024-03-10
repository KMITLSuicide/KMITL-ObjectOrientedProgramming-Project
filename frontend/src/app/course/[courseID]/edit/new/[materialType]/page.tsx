'use client';

import { useEffect, useState } from "react";
import { CourseCreateImage } from "~/src/components/course/new/image";
import { CourseCreateQuiz } from "~/src/components/course/new/quiz";
import { CourseCreateVideo } from "~/src/components/course/new/video";
import { toast } from "~/src/components/ui/use-toast";
import { getCourseLearnDataFromAPI } from "~/src/lib/data/course-learn";
import type { CourseLearn } from "~/src/lib/definitions/course";

const validTypes = ["quiz", "image", "video"];

export default function CourseViewMaterial({
  params,
}: {
  params: { courseID: string, materialType: string };
}) {
  const [courseData, setCourseData] = useState<CourseLearn | null | undefined>(undefined);
  const [materialComponent, setMaterialComponent] = useState<React.ReactNode | null>(null);

  useEffect(() => {
    async function fetchData(courseID: string) {
      const apiData = await getCourseLearnDataFromAPI(courseID);
      setCourseData(apiData);

      if (apiData === null) {
        toast({
          title: "Error",
          description: "Failed to fetch course data",
          variant: "destructive",
        })}
    }
    void fetchData(params.courseID);
  }, [params.courseID]);

  useEffect(() => {
    if (courseData !== undefined) {
      console.log(params)
      if (!validTypes.includes(params.materialType)) {
        toast({
          title: "Error",
          description: "Invalid type",
          variant: "destructive",
        });
        return;
      }

      if(params.materialType === "quiz") {
        setMaterialComponent(<CourseCreateQuiz />);
      } else if (params.materialType === "image") {
        setMaterialComponent(<CourseCreateImage courseID={params.courseID} />);
      } else if (params.materialType === "video") {
        setMaterialComponent(<CourseCreateVideo courseID={params.courseID} />);
      }
    }
  }, [courseData, params.materialType, params]);

  return (
    <div className="flex h-full flex-col space-y-2">
      {materialComponent}
    </div>
  );
}

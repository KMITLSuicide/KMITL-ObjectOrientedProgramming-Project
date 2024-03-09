'use client';

import { useEffect, useState } from "react";
import { CourseLearnImage } from "~/src/components/course/learn/image";
import { CourseLearnQuiz } from "~/src/components/course/learn/quiz";
import { CourseLearnVideo } from "~/src/components/course/learn/video";
import { toast } from "~/src/components/ui/use-toast";
import { getCourseLearnDataFromAPI } from "~/src/lib/data/course";
import type { CourseLearn } from "~/src/lib/definitions/course";

const validTypes = ["quiz", "image", "video"];

export default function CourseViewMaterial({
  params,
}: {
  params: { courseID: string, materialType: string, materialID: string};
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
        const quiz = courseData?.learn_materials_quizes.find((quiz) => quiz.id === params.materialID);
        if (quiz === undefined) {
          toast({
            title: "Error",
            description: "Invalid quiz",
            variant: "destructive",
          });
          return;
        }
        setMaterialComponent(<CourseLearnQuiz quizData={quiz} />);
      } else if (params.materialType === "image") {
        const image = courseData?.learn_materials_images.find((image) => image.id === params.materialID);
        if (image === undefined) {
          toast({
            title: "Error",
            description: "Invalid image",
            variant: "destructive",
          });
          return;
        }
        setMaterialComponent(<CourseLearnImage imageData={image} />);
      } else if (params.materialType === "video") {
        const video = courseData?.learn_materials_videos.find((video) => video.id === params.materialID);
        if (video === undefined) {
          toast({
            title: "Error",
            description: "Invalid video",
            variant: "destructive",
          });
          return;
        }
        setMaterialComponent(<CourseLearnVideo videoData={video} />);
      }
    }
  }, [courseData, params.materialID, params.materialType]);

  return (
    <div className="flex h-full flex-col space-y-2">
      {materialComponent}
    </div>
  );
}

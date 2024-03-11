'use client';

import { useEffect, useState } from "react";
import { CourseEditImage } from "~/src/components/course/edit/image";
import { CourseEditQuiz } from "~/src/components/course/edit/quiz";
import { CourseLearnVideo } from "~/src/components/course/edit/video";
import { toast } from "~/src/components/ui/use-toast";
import { getQuizKey } from "~/src/lib/data/course";
import { getCourseLearnDataFromAPI } from "~/src/lib/data/course-learn";
import type { CourseLearn, CourseLearnMaterialQuizQuestionsWithKey, CourseLearnMaterialQuizWithKey } from "~/src/lib/definitions/course";

const validTypes = ["quiz", "image", "video"];

export default function CourseViewMaterial({
  params,
}: {
  params: { courseID: string, materialType: string, materialID: string};
}) {
  const [courseData, setCourseData] = useState<CourseLearn | null | undefined>(undefined);
  const [materialComponent, setMaterialComponent] = useState<React.ReactNode | null>(null);
  const [quizKey, setQuizKey] = useState<CourseLearnMaterialQuizQuestionsWithKey[] | null | undefined>(undefined);

  async function fetchQuizKey(courseID: string, quizID: string) {
    void getQuizKey(courseID, quizID).then((response) => {
      setQuizKey(response);
    });
  }

  useEffect(() => {
    if (params.materialType === "quiz") {
      void fetchQuizKey(params.courseID, params.materialID);
    }
  }, [params.courseID, params.materialID, params.materialType]);

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
        const quizWithKey: CourseLearnMaterialQuizWithKey = {
          id: quiz.id,
          name: quiz.name,
          description: quiz.description,
          questions: quizKey ?? [],
        };
        setMaterialComponent(<CourseEditQuiz courseID={params.courseID} quizData={quizWithKey} />);
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
        setMaterialComponent(<CourseEditImage imageData={image} />);
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
  }, [courseData, params.materialID, params.materialType, params, quizKey]);

  return (
    <div className="flex h-full flex-col space-y-2">
      {materialComponent}
    </div>
  );
}

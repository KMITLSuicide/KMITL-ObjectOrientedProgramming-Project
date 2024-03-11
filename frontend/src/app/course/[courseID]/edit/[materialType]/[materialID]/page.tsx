'use client';
export const runtime = 'edge';

import { useEffect, useState } from "react";
import { CourseEditImage } from "~/src/components/course/edit/image";
import { CourseEditQuiz } from "~/src/components/course/edit/quiz";
import { CourseLearnVideo } from "~/src/components/course/edit/video";
import { toast } from "~/src/components/ui/use-toast";
import { getCourseInfoFromAPI, getQuizKey } from "~/src/lib/data/course";
import { getImageInfo, getQuizInfo, getVideoInfo } from "~/src/lib/data/course-learn";
import type { CourseInfo, CourseLearnMaterialQuizQuestionsWithKey, CourseLearnMaterialQuizWithKey } from "~/src/lib/definitions/course";

const validTypes = ["quiz", "image", "video"];

function toastErrorFetchingData() {
  toast({
    title: "Error",
    description: "Data fetching failed",
    variant: "destructive",
  });
}

export default function CourseViewMaterial({
  params,
}: {
  params: { courseID: string, materialType: string, materialID: string};
}) {
  const [courseData, setCourseData] = useState<CourseInfo | null | undefined>(undefined);
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
      const apiData = await getCourseInfoFromAPI(courseID);
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

  async function fetchData(type: string, courseID: string, materialID: string) {
    if(type === "quiz") {
      const quiz = await getQuizInfo(courseID, materialID)
      if (quiz === null) {
        toastErrorFetchingData();
        return;
      }
      const quizWithKey: CourseLearnMaterialQuizWithKey = {
        id: quiz.id,
        name: quiz.name,
        description: quiz.description,
        questions: quizKey ?? [],
      };
      return (<CourseEditQuiz courseID={params.courseID} quizData={quizWithKey} />);
    } else if (type === "image") {
      const image = await getImageInfo(courseID, materialID);
      if (image === null) {
        toastErrorFetchingData();
        return;
      }
      return (<CourseEditImage courseID={params.courseID} imageData={image} />);
    } else if (type === "video") {
      const video = await getVideoInfo(courseID, materialID);
      if (video === null) {
        toastErrorFetchingData();
        return;
      }
      return (<CourseLearnVideo courseID={params.courseID} videoData={video} />);
    }
  }

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

      void fetchData(params.materialType, params.courseID, params.materialID).then(setMaterialComponent);
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [courseData, params.courseID, params.materialID, params.materialType]);

  return (
    <div className="flex h-full flex-col space-y-2">
      {materialComponent}
    </div>
  );
}

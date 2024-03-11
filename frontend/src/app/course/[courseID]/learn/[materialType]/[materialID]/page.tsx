'use client';
export const runtime = 'edge';

import { useEffect, useState } from "react";
import { CourseLearnImage } from "~/src/components/course/learn/image";
import { CourseLearnQuiz } from "~/src/components/course/learn/quiz";
import { CourseLearnVideo } from "~/src/components/course/learn/video";
import { toast } from "~/src/components/ui/use-toast";
import { getImageInfo, getQuizInfo, getVideoInfo } from "~/src/lib/data/course-learn";

const validTypes = ["quiz", "image", "video"];

function toastErrorFetchingData() {
  toast({
    title: "Error",
    description: "Data fetching failed",
    variant: "destructive",
  });
}

async function fetchData(type: string, courseID: string, materialID: string) {
  if(type === "quiz") {
    const quiz = await getQuizInfo(courseID, materialID)
    if (quiz === null) {
      toastErrorFetchingData();
      return;
    }
    return <CourseLearnQuiz courseID={courseID} quizData={quiz} />
  } else if (type === "image") {
    const image = await getImageInfo(courseID, materialID);
    if (image === null) {
      toastErrorFetchingData();
      return;
    }
    return <CourseLearnImage imageData={image} />
  } else if (type === "video") {
    const video = await getVideoInfo(courseID, materialID);
    if (video === null) {
      toastErrorFetchingData();
      return;
    }
    return <CourseLearnVideo videoData={video} />
  }
}

export default function CourseViewMaterial({
  params,
}: {
  params: { courseID: string, materialType: string, materialID: string};
}) {
  const [materialComponent, setMaterialComponent] = useState<React.ReactNode | null>(null);

  useEffect(() => {
      if (!validTypes.includes(params.materialType)) {
        toast({
          title: "Error",
          description: "Invalid type",
          variant: "destructive",
        });
        return;
      }
      void fetchData(params.materialType, params.courseID, params.materialID).then(setMaterialComponent);
    }, [params.courseID, params.materialID, params.materialType]);

  return (
    <div className="flex h-full flex-col space-y-2">
      {materialComponent}
    </div>
  );
}

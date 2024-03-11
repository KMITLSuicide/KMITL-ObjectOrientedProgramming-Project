"use client";

import { useEffect, useState } from "react";
import { toast } from "~/src/components/ui/use-toast";
import { getCourseLearnDataFromAPI } from "~/src/lib/data/course-learn";
import { type CourseLearn } from "~/src/lib/definitions/course";

export default function CourseEdit({
  params,
}: {
  params: { courseID: string };
}) {
  const [learnData, setLearnData] = useState<CourseLearn | null | undefined>(
    undefined,
  );
  useEffect(() => {
    void getCourseLearnDataFromAPI(params.courseID).then((data) => {
      setLearnData(data);
      if (data === null) {
        toast({
          title: "Error",
          description: "Failed to fetch data",
          variant: "destructive",
        })}
    });
  }, [params.courseID]);

  return (
    <div className="flex flex-col space-y-2">
      <h4 className="text-lg bg-destructive text-destructive-foreground w-fit p-2 rounded-md">Editing</h4>
      <h1 className="text-4xl font-bold">{learnData?.name}</h1>
      <p className="text-lg">{learnData?.description}</p>
    </div>
  );
}

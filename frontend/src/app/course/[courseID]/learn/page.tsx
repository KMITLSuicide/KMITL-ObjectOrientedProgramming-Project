"use client";
export const runtime = 'edge';

import { useEffect, useState } from "react";
import { toast } from "~/src/components/ui/use-toast";
import { getCourseInfoFromAPI } from "~/src/lib/data/course";
import type { CourseInfo } from "~/src/lib/definitions/course";

export default function CourseLearn({
  params,
}: {
  params: { courseID: string };
}) {
  const [learnData, setLearnData] = useState<CourseInfo | null | undefined>(
    undefined,
  );
  useEffect(() => {
    void getCourseInfoFromAPI(params.courseID).then((data) => {
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
      <h4 className="text-lg font-light">Learning</h4>
      <h1 className="text-4xl font-bold">{learnData?.name}</h1>
      <p className="text-lg">{learnData?.description}</p>
      <p className="text-base font-light">
        Please choose course material on the sidebar.
      </p>
    </div>
  );
}

"use client";
export const runtime = 'edge';

import { useEffect, useState } from "react";
import { toast } from "~/src/components/ui/use-toast";
import { getCourseInfoFromAPI } from "~/src/lib/data/course";
import type { CourseInfo } from "~/src/lib/definitions/course";
import { CourseEdit } from "~/src/components/course/edit/course";

export default function CourseEditPage({
  params,
}: {
  params: { courseID: string };
}) {
  const [courseInfo, setCourseInfo] = useState<CourseInfo | null | undefined>(
    undefined,
  );
  useEffect(() => {
    void getCourseInfoFromAPI(params.courseID).then((data) => {
      setCourseInfo(data);
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
      {courseInfo && <CourseEdit courseInfo={courseInfo} />}
    </div>
  );
}

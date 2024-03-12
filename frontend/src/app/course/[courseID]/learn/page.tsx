"use client";
export const runtime = 'edge';

import Link from "next/link";
import { useEffect, useState } from "react";
import { Button } from "~/src/components/ui/button";
import { toast } from "~/src/components/ui/use-toast";
import { getCourseInfoFromAPI } from "~/src/lib/data/course";
import type { CourseInfo } from "~/src/lib/definitions/course";

export default function CourseLearn({
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
      <h4 className="text-lg font-light">Learning</h4>
      <h1 className="text-4xl font-bold">{courseInfo?.name}</h1>
      <p className="text-lg">{courseInfo?.description}</p>
      <p className="text-base font-light">
        Please choose course material on the sidebar.
      </p>
      <Button asChild className="w-fit">
        <Link href={`/course/${courseInfo?.id}`}>
          Write a review!
        </Link>
      </Button>
    </div>
  );
}

"use client";

import { useEffect, useState } from "react";
import { CourseCard } from "~/src/components/course/card";
import { toast } from "~/src/components/ui/use-toast";
import { getMyLearnings } from "~/src/lib/data/account/learning";
import { getProgressNormalized } from "~/src/lib/data/course-learn";
import type { CourseCardDataWithProgress, CourseCardData } from "~/src/lib/definitions/course";

export default function MyTeachings() {
  const [baseCardsData, setBaseCardsData] = useState<
    CourseCardData[] | null | undefined
  >(undefined);
  const [cardsDataProgress, setCardsDataProgress] = useState<
    CourseCardDataWithProgress[] | null | undefined
  >(undefined);

  useEffect(() => {
    async function fetchData() {
      const apiData = await getMyLearnings();
      setBaseCardsData(apiData);

      if (apiData === null) {
        toast({
          title: "Error",
          description: "Failed to fetch my teachings",
          variant: "destructive",
        })}
    }
    void fetchData();
  }, []);

  async function addProgressToCard(course: CourseCardData) {
    const progress = await getProgressNormalized(course.id);
    if (progress === null) {
      toast({
        title: "Error",
        description: "Failed to fetch progress",
        variant: "destructive",
      });
      return;
    }
    setCardsDataProgress((prev) => {
      // Check if a card with the same course id already exists
      if (prev?.some((card) => card.id === course.id)) {
        return prev;
      }
      return [
        ...(prev ?? []),
        {
          ...course,
          progress: progress,
        },
      ];
    });
  }

  useEffect(() => {
    if (baseCardsData === undefined) {
      return;
    }

    baseCardsData?.map((course) => {
      void addProgressToCard(course);
    });
  }, [baseCardsData]);

  return (
    <div className="flex w-full justify-center">
      <div className="w-full max-w-screen-lg space-y-4">
        <h1 className="text-3xl font-bold">My Learnings</h1>
        <div className="grid grid-cols-4 gap-4">
          {cardsDataProgress?.map((course) => {
            return <CourseCard key={course.id} course={course} customLink={`/course/${course.id}/learn`} showPrice={false} progress={course.progress} />;
          })}
        </div>
      </div>
    </div>
  );
}

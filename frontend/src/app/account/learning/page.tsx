"use client";

import { useEffect, useState } from "react";
import { CourseCard } from "~/src/components/course/card";
import { toast } from "~/src/components/ui/use-toast";
import { getMyLearnings } from "~/src/lib/data/account/learning";
import { type CourseCardData } from "~/src/lib/definitions/course";

export default function MyTeachings() {
  const [cardsData, setCardsData] = useState<
    CourseCardData[] | null | undefined
  >(undefined);

  useEffect(() => {
    async function fetchData() {
      const apiData = await getMyLearnings();
      setCardsData(apiData);

      if (apiData === null) {
        toast({
          title: "Error",
          description: "Failed to fetch my teachings",
          variant: "destructive",
        })}
    }
    void fetchData();
  }, []);

  return (
    <div className="flex w-full justify-center">
      <div className="w-full max-w-screen-lg space-y-4">
        <h1 className="text-3xl font-bold">My Learnings</h1>
        <div className="grid grid-cols-4 gap-4">
          {cardsData?.map((course) => {
            return <CourseCard key={course.id} course={course} customLink={`/course/${course.id}/edit`} />;
          })}
        </div>
      </div>
    </div>
  );
}

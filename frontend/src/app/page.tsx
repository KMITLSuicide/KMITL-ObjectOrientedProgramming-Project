"use client";

import Image from "next/image";
import { useEffect, useState } from "react";
import { CourseCard } from "~/src/components/course/card";
import { toast } from "~/src/components/ui/use-toast";
import { getReccommendedCourses } from "~/src/lib/data/homepage";
import { type CourseCardData } from "~/src/lib/definitions/course";

export default function Index() {
  const [cardsData, setCardsData] = useState<
    CourseCardData[] | null | undefined
  >(undefined);

  useEffect(() => {
    async function fetchData() {
      const apiData = await getReccommendedCourses();
      setCardsData(apiData);

      if (apiData === null) {
        toast({
          title: "Error",
          description: "Failed to fetch recommended courses",
          variant: "destructive",
        });
      }
    }
    void fetchData();
  }, []);

  return (
    <div className="flex h-full w-full items-center justify-center">
      <div className="flex h-full w-full max-w-screen-lg flex-col items-center justify-center space-y-4">
        <div className="grid grid-cols-[1fr_2fr] h-2/5 w-full flex-col">
          <div className="relative h-full">
            <Image
              className="absolute object-contain"
              src="/pointy-guy.png"
              alt="pointy guy"
              fill
            />
          </div>
          <div className="flex flex-col">
            <div className="flex flex-grow">
            </div>
            <div className="w-full space-y-2 bg-primary p-8">
              <h1 className="fle text-4xl font-bold">
                Welcome to &quot;Udemy&quot;
              </h1>
              <p className="text-xl">
                A place that have &quot;courses&quot; where you can technically
                &quot;buy&quot; <br /> from some random and &quot;learn&quot;.
              </p>
            </div>
          </div>
        </div>

        <div className="w-3/4 space-y-2">
          <h2 className="text-center text-3xl font-semibold">
            Recommended courses
          </h2>
          <div className="grid grid-cols-3 gap-4">
            {cardsData?.map((course) => {
              return <CourseCard key={course.id} course={course} />;
            })}
          </div>
        </div>
      </div>
    </div>
  );
}

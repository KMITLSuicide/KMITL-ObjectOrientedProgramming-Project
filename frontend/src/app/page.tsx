'use client';

import Image from "next/image"
import { useEffect, useState } from "react";
import { CourseCard } from "~/src/components/course/card";
import { getReccommendedCourses } from "~/src/lib/data/homepage";
import { type CourseCardData } from "~/src/lib/definitions/course";

export default function Index() {
  const [cardsData, setCardsData] = useState<CourseCardData[] | null | undefined>(undefined);

  useEffect(() => {
    async function fetchData() {
      const apiData = await getReccommendedCourses();
      console.log(apiData);
      setCardsData(apiData);
    }
    void fetchData();
  }, []);

  return (
    <div className="h-full w-full flex justify-center items-center">
      <div className="h-full w-full max-w-screen-lg flex flex-col justify-center items-center space-y-4 mb-24">
        <div className="flex flex-grow"></div>

        <div className="w-full flex h-1/5 bg-primary rounded-xl p-8">
          <div className="w-2/5 inline-block">
            <Image className="absolute left-[23vw] top-[6vh]" src="/pointy-guy.png" alt="pointy guy" width={360} height={544} />
          </div>
          <div className="w-3/5 space-y-2">
            <h1 className="text-4xl font-bold fle">Welcome to &quot;Udemy&quot;</h1>
            <p className="text-xl">
              A place that have &quot;courses&quot; where you can technically &quot;buy&quot; <br /> from some random and &quot;learn&quot;.
            </p>
          </div>
        </div>

        <div className="w-3/4 space-y-2">
          <h2 className="text-center font-semibold text-3xl">Reccommended courses</h2>
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

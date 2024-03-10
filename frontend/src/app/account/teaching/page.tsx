"use client";

import { useEffect, useState } from "react";
import { CourseCard } from "~/src/components/course/card";
import { Button } from "~/src/components/ui/button";
import { toast } from "~/src/components/ui/use-toast";
import { getMyTeachings } from "~/src/lib/data/account/teaching";
import { type CourseCardData } from "~/src/lib/definitions/course";
import { Plus } from 'lucide-react';
import Link from "next/link";

export default function MyTeachings() {
  const [cardsData, setCardsData] = useState<
    CourseCardData[] | null | undefined
  >(undefined);

  useEffect(() => {
    async function fetchData() {
      const apiData = await getMyTeachings();
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
        <div className="flex flex-row justify-between">
          <h1 className="text-3xl font-bold">My Teachings</h1>
          <Button asChild>
            <Link href="/course/create">
              <Plus className="mr-2 h-6 w-6" />
              <p>Create Course</p>
            </Link>
          </Button>
        </div>
        <div className="grid grid-cols-4 gap-4">
          {cardsData?.map((course) => {
            return <CourseCard key={course.id} course={course} customLink={`/course/${course.id}/edit`} />;
          })}
        </div>
      </div>
    </div>
  );
}

"use client";

import { useEffect, useState } from "react";
import { getCategoryDataWithIDFromAPI } from "~/src/lib/data/category";
import { type CategoryInfo } from "~/src/lib/definitions/category";
import { CourseCard } from "~/src/components/course/card";

export default function CategoryIDPage({
  params,
}: {
  params: { categoryID: string };
}) {
  const [categoryIDData, setCategoryIDData] = useState<
    CategoryInfo | null | undefined
  >(undefined);

  useEffect(() => {
    async function fetchData() {
      const apiData = await getCategoryDataWithIDFromAPI(params.categoryID);
      console.log(apiData);
      setCategoryIDData(apiData);
    }
    void fetchData();
  }, []);

  return (
    <div className="flex w-full justify-center">
      <div className="w-full max-w-screen-lg space-y-4">
        <h1 className="text-3xl font-bold">{categoryIDData?.name}</h1>
        <div className="grid grid-cols-4 gap-4">
          {categoryIDData?.courses?.map((course) => {
            return <CourseCard key={course.id} course={course} />;
          })}
        </div>
      </div>
    </div>
  );
}

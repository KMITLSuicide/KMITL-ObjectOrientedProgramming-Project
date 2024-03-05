'use client';

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { getCategoryDataWithIDFromAPI } from "~/src/lib/data/category";
import {
  Card,
  CardContent,
  CardDescription,
  // CardFooter,
  CardHeader,
  CardTitle,
} from "~/src/components/ui/card";
import { type CourseCategory } from "~/src/lib/definitions/course";

export default function CategoryIDPage({
  params,
}: {
  params: { categoryID: string };
}) {
  const [categoryIDData, setCategoryIDData] = useState<
    CourseCategory | null | undefined
  >(undefined);
  const router = useRouter();

  useEffect(() => {
    async function fetchData() {
      const apiData = await getCategoryDataWithIDFromAPI(params.categoryID);
      console.log(apiData);
      setCategoryIDData(apiData);
    }
    void fetchData();
  }, []);

  return (
    <div className="flex justify-center w-full">
      <div className="w-full max-w-screen-lg space-y-4">
        <h1 className="font-bold text-3xl">{categoryIDData?._CourseCategory__name}</h1>
        <div className="grid grid-cols-4 gap-4">
          {categoryIDData?._CourseCategory__courses?.map((course) => {
            return (
              <Card
                className="w-full cursor-pointer hover:bg-secondary "
                key={course._Course__id}
                onClick={() => router.push(`/course/${course._Course__id}`)}
              >
                <CardHeader>
                  <CardTitle>{course._Course__name}</CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription>{course._Course__description}</CardDescription>
                </CardContent>
              </Card>
            );
          })}
        </div>
        {/* <code>
          {JSON.stringify(categoryIDData, null, 2)}
        </code> */}
      </div>
    </div>
  );
}
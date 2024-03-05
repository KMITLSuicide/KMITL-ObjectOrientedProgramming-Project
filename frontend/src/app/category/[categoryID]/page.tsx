'use client';

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { type CategoryData, getCategoryDataWithIDFromAPI } from "~/src/lib/data/category";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "~/src/components/ui/card";

export default function CategoryIDPage({
  params,
}: {
  params: { categoryID: string };
}) {
  const [categoryIDData, setCategoryIDData] = useState<
    CategoryData | null | undefined
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
        <div className="flex flex-wrap justify-between">
          {categoryIDData?._CourseCategory__courses?.map((course) => {
            return (
              <Card className="w-1/5 m-4" key={course._Course__id}>
                <CardHeader>
                  <CardTitle>{course._Course__name}</CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription>{course._Course__description}</CardDescription>
                </CardContent>
                {/* <CardFooter className="flex justify-between">
                </CardFooter> */}
              </Card>
            );
          })}
          {categoryIDData?._CourseCategory__courses?.map((course) => {
            return (
              <Card className="w-1/5 m-4" key={course._Course__id}>
                <CardHeader>
                  <CardTitle>{course._Course__name}</CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription>{course._Course__description}</CardDescription>
                </CardContent>
                {/* <CardFooter className="flex justify-between">
                </CardFooter> */}
              </Card>
            );
          })}

          <Card className="w-1/5 m-4">
            <CardHeader>
              <CardTitle>name</CardTitle>
            </CardHeader>
            <CardContent>
              <CardDescription>description</CardDescription>
            </CardContent>
            {/* <CardFooter className="flex justify-between">
            </CardFooter> */}
          </Card>
          <Card className="w-1/5 m-4">
            <CardHeader>
              <CardTitle>name</CardTitle>
            </CardHeader>
            <CardContent>
              <CardDescription>description</CardDescription>
            </CardContent>
            {/* <CardFooter className="flex justify-between">
            </CardFooter> */}
          </Card>
        </div>
        {/* <code>
          {JSON.stringify(categoryIDData, null, 2)}
        </code> */}
      </div>
    </div>
  );
}
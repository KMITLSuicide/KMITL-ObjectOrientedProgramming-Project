"use client";

import { ChevronsUpDown } from "lucide-react";
import Image from "next/image";
import React, { useEffect } from "react";
import { Button } from "~/src/components/ui/button";
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "~/src/components/ui/collapsible";
import { ScrollArea } from "~/src/components/ui/scroll-area";
import { Config } from "~/src/config";
import { getCourseDataWithIDFromAPI } from "~/src/lib/data/course";
import { type Course } from "~/src/lib/definitions/course";

// export function getFrontendCourseViewData(courseID: string) {
//   const imageNumber = (courseID.charCodeAt(0) % 6) + 1;
//   const quizNumber = courseID.charCodeAt(0);
//   return {
//     id: courseID,
//     name: "course name",
//     description: "course description",
//     category: {
//       courses: [],
//       id: "category id",
//       name: "category name",
//     },
//     price: 10000,
//     images: [
//       {
//         id: courseID + `image-${imageNumber}`,
//         name: "image name",
//         description: "image description",
//         url: `/course/react/image-${imageNumber}.png`,
//       },
//     ],
//     quizes: [
//       {
//         id: courseID + `quiz-${quizNumber}`,
//         name: "quiz name",
//         description: "quiz description",
//         questions: [
//           {
//             question: `quiz-${quizNumber}`,
//           },
//         ],
//       },
//     ],
//   };
// }

export default function CourseView({
  params,
}: {
  params: { courseID: string };
}) {
  const [courseContentOpen, setCourseContentOpen] = React.useState(false);
  const [courseQuizOpen, setCourseQuizOpen] = React.useState(false);
  const [courseData, setCourseData] = React.useState<Course | null>(null);

  useEffect(() => {
    async function fetchData(courseID: string) {
      const apiData = await getCourseDataWithIDFromAPI(courseID);
      console.log(apiData);
      setCourseData(apiData);
    }
    void fetchData(params.courseID);
  }, []);

  return (
    <div className="flex h-full w-full justify-center">
      <div className="flex w-full max-w-screen-xl justify-center">
        <div className="flex w-3/5 flex-col space-y-4">
          {/* <p className="w-fit rounded-full bg-secondary p-2 px-4">
            {courseData?.}
          </p> */}

          <h1 className="text-3xl">
            <b>{courseData?._Course__name}</b>
          </h1>

          <p className="text-lg">{courseData?._Course__description}</p>

          <div className="flex w-full flex-col justify-normal space-y-3">
            <h2 className="text-xl">
              <b>In this course:</b>
            </h2>
          </div>

          <div>
            <Collapsible
              open={courseContentOpen}
              onOpenChange={setCourseContentOpen}
              className="w-max space-y-2"
            >
              <div className="flex items-center justify-between space-x-4 rounded-md border p-2 px-4">
                <h4 className="text-sm font-semibold">Course contents</h4>
                <CollapsibleTrigger asChild>
                  <Button variant="ghost" size="sm" className="w-9 p-0">
                    <ChevronsUpDown className="h-4 w-4" />
                    <span className="sr-only">Toggle</span>
                  </Button>
                </CollapsibleTrigger>
              </div>
              <CollapsibleContent className="space-y-2">
                <ul className="ml-10 list-decimal">
                  {courseData?._Course__images.map((element, index) => {
                    return (
                      <li key={index} className="rounded-md px-2 text-sm">
                        {element._CourseMaterial__name}
                      </li>
                    );
                  })}
                </ul>
              </CollapsibleContent>
            </Collapsible>
          </div>

          <Collapsible
            open={courseQuizOpen}
            onOpenChange={setCourseQuizOpen}
            className="w-max space-y-2"
          >
            <div className="flex items-center justify-between space-x-4 rounded-md border p-2 px-4">
              <h4 className="text-sm font-semibold">Course quizes</h4>
              <CollapsibleTrigger asChild>
                <Button variant="ghost" size="sm" className="w-9 p-0">
                  <ChevronsUpDown className="h-4 w-4" />
                  <span className="sr-only">Toggle</span>
                </Button>
              </CollapsibleTrigger>
            </div>
            <CollapsibleContent className="space-y-2">
              <ul className="ml-10 list-decimal">
                {courseData?._Course__quizes.map((element, index) => {
                  return (
                    <li key={index} className="rounded-md px-2 text-sm">
                      {element._CourseMaterial__name}
                    </li>
                  );
                })}
              </ul>
            </CollapsibleContent>
          </Collapsible>
        </div>
        <div className="flex h-fit w-2/5 rounded-lg bg-secondary p-4">
          <div className="flex flex-col items-center justify-center space-y-4">
            <Image
              className="rounded-md"
              src={courseData?._Course__images[0]?._CourseMaterialImage__url ?? "/notexture.png"}
              alt="course hero image"
              width={1920}
              height={1080}
              sizes="100%"
            />

            <div className="flex items-center justify-center rounded-md p-4 text-xl outline">
              <h3 className="text-2xl">
                <b>
                  {courseData?._Course__price.toLocaleString(Config.locale, {
                    style: "currency",
                    currency: Config.currency,
                    minimumFractionDigits: 0,
                  })}
                </b>
              </h3>
            </div>

            <div className="flex w-full justify-center space-x-6">
              <Button variant="outline">Add to cart</Button>
              <Button variant="default">Buy now!</Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

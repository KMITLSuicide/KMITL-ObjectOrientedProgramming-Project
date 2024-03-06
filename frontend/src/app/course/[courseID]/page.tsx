"use client";

import { ChevronsUpDown } from "lucide-react";
import Image from "next/image";
import Link from "next/link";
import React, { useEffect } from "react";
import { Button } from "~/src/components/ui/button";
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "~/src/components/ui/collapsible";
import { Config } from "~/src/config";
import { getCourseInfoFromAPI } from "~/src/lib/data/course";
import { type CourseInfo } from "~/src/lib/definitions/course";

export default function CourseView({
  params,
}: {
  params: { courseID: string };
}) {
  const [courseContentOpen, setCourseContentOpen] = React.useState(false);
  const [courseQuizOpen, setCourseQuizOpen] = React.useState(false);
  const [courseVideoOpen, setCourseVideosOpen] = React.useState(false);
  const [courseData, setCourseData] = React.useState<CourseInfo | null>(null);

  useEffect(() => {
    async function fetchData(courseID: string) {
      const apiData = await getCourseInfoFromAPI(courseID);
      console.log(apiData);
      setCourseData(apiData);
    }
    void fetchData(params.courseID);
  }, []);

  return (
    <div className="flex h-full w-full justify-center">
      <div className="flex w-full max-w-screen-xl justify-center">
        <div className="flex w-3/5 flex-col space-y-4">
          <Button asChild className="w-fit rounded-full bg-secondary text-secondary-foreground p-2 px-4">
            <Link href={`/category/${courseData?.category_id}`}>{courseData?.category_name}</Link>
          </Button>

          <h1 className="text-3xl">
            <b>{courseData?.name}</b>
          </h1>

          <p className="text-lg">{courseData?.description}</p>

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
                  {courseData?.materials_images.map((name, index) => {
                    return (
                      <li key={index} className="rounded-md px-2 text-sm">
                        {name}
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
                {courseData?.materials_quizes.map((name, index) => {
                  return (
                    <li key={index} className="rounded-md px-2 text-sm">
                      {name}
                    </li>
                  );
                })}
              </ul>
            </CollapsibleContent>
          </Collapsible>

          <Collapsible
            open={courseVideoOpen}
            onOpenChange={setCourseVideosOpen}
            className="w-max space-y-2"
          >
            <div className="flex items-center justify-between space-x-4 rounded-md border p-2 px-4">
              <h4 className="text-sm font-semibold">Course videos</h4>
              <CollapsibleTrigger asChild>
                <Button variant="ghost" size="sm" className="w-9 p-0">
                  <ChevronsUpDown className="h-4 w-4" />
                  <span className="sr-only">Toggle</span>
                </Button>
              </CollapsibleTrigger>
            </div>
            <CollapsibleContent className="space-y-2">
              <ul className="ml-10 list-decimal">
                {courseData?.materials_videos.map((name, index) => {
                  return (
                    <li key={index} className="rounded-md px-2 text-sm">
                      {name}
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
              src={courseData?.banner_image ?? "/notexture.png"}
              alt="course hero image"
              width={1920}
              height={1080}
              sizes="100%"
            />

            <div className="flex items-center justify-center rounded-md p-4 text-xl outline">
              <h3 className="text-2xl">
                <b>
                  {courseData?.price.toLocaleString(Config.locale, {
                    style: "currency",
                    currency: Config.currency,
                    minimumFractionDigits: 0,
                  })}
                </b>
              </h3>
            </div>

            <div className="flex w-full justify-center space-x-6">
              <Button variant="link">Add to cart</Button>
              <Button variant="default">Buy now!</Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

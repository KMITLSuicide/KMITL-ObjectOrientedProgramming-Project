"use client";

import { ChevronsUpDown } from "lucide-react";
import Image from "next/image";
import React from "react";
import { Button } from "~/src/components/ui/button";
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "~/src/components/ui/collapsible";
import { ScrollArea } from "~/src/components/ui/scroll-area";
import { Config } from "~/src/config";
import { getFrontendCourseViewData } from "~/src/lib/data/course";

export default function CourseView({
  params,
}: {
  params: { courseID: string };
}) {
  const [courseContentOpen, setCourseContentOpen] = React.useState(false);
  const [courseQuizOpen, setCourseQuizOpen] = React.useState(false);
  const courseData = getFrontendCourseViewData(params.courseID);

  return (
    <div className="flex h-full w-full justify-center">
      <div className="flex w-full max-w-screen-xl justify-center">
        <div className="flex flex-col w-3/5 space-y-4">
          <p className="bg-secondary w-fit p-2 px-4 rounded-full">
            {courseData.category.name}
          </p>

          <h1 className="text-3xl">
            <b>{courseData.name}</b>
          </h1>

          <p className="text-lg">{courseData.description}</p>

          <div className="flex w-full flex-col justify-normal space-y-3">
            <h2 className="text-xl"><b>In this course:</b></h2>
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
                <ul className="list-decimal ml-10">
                  {courseData.images.map((element, index) => {
                    return (
                      <li key={index} className="rounded-md px-2 text-sm">
                        {element.name}
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
              <ul className="list-decimal ml-10">
                {courseData.quizes.map((element, index) => {
                  return (
                    <li key={index} className="rounded-md px-2 text-sm">
                      {element.name}
                    </li>
                  );
                })}
              </ul>
            </CollapsibleContent>
          </Collapsible>
        </div>
        <div className="flex w-2/5 h-fit p-4 bg-secondary rounded-lg">
          <div className="flex flex-col items-center justify-center space-y-4">
            <Image
              className="rounded-md"
              src={courseData.images[0]?.url ?? "/notexture.png"}
              alt="course hero image"
              width={1920}
              height={1080}
              sizes="100%"
            />

            <div className="flex items-center justify-center rounded-md p-4 text-xl outline">
              <h3 className="text-2xl">
                <b>
                  {courseData.price.toLocaleString(Config.locale, {
                    style: "currency",
                    currency: Config.currency,
                    minimumFractionDigits: 0,
                  })}
                </b>
              </h3>
            </div>

            <div className="flex w-full justify-center space-x-6">
              <Button variant='outline'>
                Add to cart
              </Button>
              <Button variant='default'>
                Buy now!
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

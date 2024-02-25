'use client';

import { ChevronsUpDown } from "lucide-react";
import Image from "next/image";
import React from "react";
import { Button } from "~/src/components/ui/button";
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "~/src/components/ui/collapsible";
import { Config } from "~/src/config";
import { getFrontendCourseViewData } from "~/src/lib/data/course";

export default function CourseLearn({
  params,
}: {
  params: { courseID: string };
}) {
  const [courseContentOpen, setCourseContentOpen] = React.useState(false);
  const [courseQuizOpen, setCourseQuizOpen] = React.useState(false);
  const courseData = getFrontendCourseViewData(params.courseID);

  return (
    <div className="flex justify-center">
      <div className="flex flex-col space-y-4 justify-center items-center max-w-screen-lg">
        <Image className="rounded-md" src={courseData.images[0]?.url ?? '/notexture.png'} alt="course hero image" width={1024} height={720} />

        <div className="flex justify-between space-x-8">
          <div className="flex bg-primary text-primary-foreground justify-center items-center text-xl p-4 rounded-md">
            <h3><b>{courseData.price.toLocaleString(Config.locale, {style: 'currency', currency: Config.currency, minimumFractionDigits: 0})}</b></h3>
          </div>
          <div className="flex justify-center items-center">
            <h1 className="text-3xl"><b>{courseData.name}</b></h1>
          </div>
        </div>
        <p className="text-base">{courseData.description}</p>

        <div className="flex flex-col space-y-3 justify-normal w-full">
          <h2 className="text-xl">In this course:</h2>

          <Collapsible
            open={courseContentOpen}
            onOpenChange={setCourseContentOpen}
            className="w-max space-y-2"
          >
            <div className="flex items-center justify-between space-x-4 px-4 border rounded-md p-2">
              <h4 className="text-sm font-semibold">
                Course contents
              </h4>
              <CollapsibleTrigger asChild>
                <Button variant="ghost" size="sm" className="w-9 p-0">
                  <ChevronsUpDown className="h-4 w-4" />
                  <span className="sr-only">Toggle</span>
                </Button>
              </CollapsibleTrigger>
            </div>
            <CollapsibleContent className="space-y-2">
              {courseData.images.map((element, index) => {
                return (
                  <div key={index} className="rounded-md px-4 text-sm">
                    {element.name}
                  </div>
                );
              })}
            </CollapsibleContent>
          </Collapsible>

          <Collapsible
            open={courseQuizOpen}
            onOpenChange={setCourseQuizOpen}
            className="w-max space-y-2"
          >
            <div className="flex items-center justify-between space-x-4 px-4 border rounded-md p-2">
              <h4 className="text-sm font-semibold">
                Course quizes
              </h4>
              <CollapsibleTrigger asChild>
                <Button variant="ghost" size="sm" className="w-9 p-0">
                  <ChevronsUpDown className="h-4 w-4" />
                  <span className="sr-only">Toggle</span>
                </Button>
              </CollapsibleTrigger>
            </div>
            <CollapsibleContent className="space-y-2">
              {courseData.quizes.map((element, index) => {
                return (
                  <div key={index} className="rounded-md px-4 text-sm">
                    {element.name}
                  </div>
                );
              })}
            </CollapsibleContent>
          </Collapsible>
        </div>
      </div>
    </div>
  );
}

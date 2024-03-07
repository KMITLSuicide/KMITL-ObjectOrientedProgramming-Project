"use client";

import { useEffect, useState } from "react";
import CourseLearnSidebar, {
  type SidebarCategory,
  type SidebarItem,
} from "~/src/components/course/sidebar";
import { ScrollArea } from "~/src/components/ui/scroll-area";
import { getCourseLearnDataFromAPI } from "~/src/lib/data/course";
import { type CourseLearn } from "~/src/lib/definitions/course";
import { useToast } from "~/src/components/ui/use-toast";
import Link from "next/link";
import { Button } from "~/src/components/ui/button";

export default function CourseLearnLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: { courseID: string };
}) {
  const { toast } = useToast();
  const [learnData, setLearnData] = useState<CourseLearn | null | undefined>(
    undefined,
  );
  useEffect(() => {
    void getCourseLearnDataFromAPI(params.courseID).then((data) => {
      setLearnData(data);
    });
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    if (learnData === null) {
      toast({
        title: "Access Denied",
        description: "You don't have access to this course.",
        variant: "destructive",
      });
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [learnData]);

  const sidebarImagesItems = learnData?.learn_materials_images.map(
    (element): SidebarItem => {
      return {
        name: element.name,
        link: `/course/${params.courseID}/learn/image/${element.id}`,
      };
    },
  );
  const sidebarQuizItems = learnData?.learn_materials_quizes.map(
    (element): SidebarItem => {
      return {
        name: element.name,
        link: `/course/${params.courseID}/learn/quiz/${element.id}`,
      };
    },
  );
  const sidebarVideosItems = learnData?.learn_materials_videos.map(
    (element): SidebarItem => {
      return {
        name: element.name,
        link: `/course/${params.courseID}/learn/video/${element.id}`,
      };
    },
  );

  const sidebarCategories: SidebarCategory[] = [
    {
      name: "Images",
      sidebarItems: sidebarImagesItems ?? [],
    },
    {
      name: "Quizes",
      sidebarItems: sidebarQuizItems ?? [],
    },
    {
      name: "Videos",
      sidebarItems: sidebarVideosItems ?? [],
    },
  ];

  return (
    <div className="flex h-full w-full justify-center">
      <div className="flex w-full max-w-screen-xl space-x-6">
        <ScrollArea className="h-full w-4/5 rounded-xl bg-secondary p-6">
          {children}
        </ScrollArea>
        <div className="h-full w-1/5">
          <Button
            asChild
            className="w-full rounded-lg bg-primary px-4 py-2 text-xl font-bold text-left justify-normal"
          >
            <Link href={`/course/${learnData?.id}/learn`}>
              {learnData?.name}
            </Link>
          </Button>
          <CourseLearnSidebar
            className="px-5"
            sidebarCategories={sidebarCategories}
          />
        </div>
      </div>
    </div>
  );
}

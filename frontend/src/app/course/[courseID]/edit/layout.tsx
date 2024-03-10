"use client";

import { useEffect, useState } from "react";
import CourseLearnSidebar, {
  type SidebarCategory,
  type SidebarItem,
} from "~/src/components/course/sidebar";
import { getCourseLearnDataFromAPI } from "~/src/lib/data/course";
import { type CourseLearn } from "~/src/lib/definitions/course";
import { useToast } from "~/src/components/ui/use-toast";
import Link from "next/link";
import { Button } from "~/src/components/ui/button";
import { Book, Plus, SquarePen } from "lucide-react";
import { useSearchParams } from "next/navigation";

export default function CourseLearnLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: { courseID: string };
}) {
  const searchParams = useSearchParams();
  const { toast } = useToast();
  const [learnData, setLearnData] = useState<CourseLearn | null | undefined>(
    undefined,
  );

  async function fetchData(courseID: string) {
    const data = await getCourseLearnDataFromAPI(courseID);
    setLearnData(data);
    if (data === null) {
      toast({
        title: "Error",
        description: "Failed to fetch data",
        variant: "destructive",
      })}
  }

  useEffect(() => {
    void fetchData(params.courseID);
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [params.courseID]);

  if (searchParams.has("fetch")) {
    void fetchData(params.courseID);
  }

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
        link: `/course/${params.courseID}/edit/image/${element.id}`,
      };
    },
  );
  const sidebarQuizItems = learnData?.learn_materials_quizes.map(
    (element): SidebarItem => {
      return {
        name: element.name,
        link: `/course/${params.courseID}/edit/quiz/${element.id}`,
      };
    },
  );
  const sidebarVideosItems = learnData?.learn_materials_videos.map(
    (element): SidebarItem => {
      return {
        name: element.name,
        link: `/course/${params.courseID}/edit/video/${element.id}`,
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
        <div className="h-full w-4/5 rounded-xl bg-secondary p-8">
          {children}
        </div>
        <div className="h-full w-1/5 space-y-2">
          <div className="flex space-x-2">
            <Button
              asChild
              className="flex-grow justify-normal rounded-lg bg-primary px-4 py-2 text-left text-xl font-bold space-x-2"
            >
              <Link href={`/course/${learnData?.id}/edit`}>
              <SquarePen />
              <p>
                {learnData?.name}
              </p>
              </Link>
            </Button>

            <Button
              asChild
              className=""
              size='icon'
            >
              <Link href={`/course/${learnData?.id}/learn`}>
                <Book />
              </Link>
          </Button>
          </div>

          <div className="flex">
            <Button
              asChild
              className="flex-grow justify-normal rounded-lg bg-primary px-4 py-2 text-left text-lg font-semibold space-x-2"
            >
              <Link href={`/course/${learnData?.id}/edit/new`} className="flex">
                <Plus />
                <p>
                  New material
                </p>
              </Link>
            </Button>
          </div>

          <CourseLearnSidebar
            className="px-5"
            sidebarCategories={sidebarCategories}
          />
        </div>
      </div>
    </div>
  );
}

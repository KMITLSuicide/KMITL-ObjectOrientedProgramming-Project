"use client";

import { useEffect, useState } from "react";
import CourseLearnSidebar, {
  type SidebarCategory,
  type SidebarItem,
} from "~/src/components/course/sidebar";
import { type CourseLearn } from "~/src/lib/definitions/course";
import { useToast } from "~/src/components/ui/use-toast";
import Link from "next/link";
import { Button } from "~/src/components/ui/button";
import { Book } from "lucide-react";
import {
  getCourseLearnDataFromAPI,
  getNormalizedProgress,
} from "~/src/lib/data/course-learn";
import { Progress as ProgressBar } from "~/src/components/ui/progress";
import { useSearchParams } from "next/navigation";
import type { Progress as ProgressType } from "~/src/lib/definitions/course-learn";

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
  const [progressTotal, setProgressTotal] = useState<number>(0);
  const [progressNormalizedImage, setProgressNormalizedImage] =
    useState<number>(0);
  const [progressNormalizedQuiz, setProgressNormalizedQuiz] =
    useState<number>(0);
  const [progressNormalizedVideo, setProgresNormalizedVideo] =
    useState<number>(0);
  const [progressQuiz, setProgressQuiz] = useState<ProgressType[] | undefined>(
    undefined,
  );
  const [progressVideo, setProgresVideo] = useState<ProgressType[] | undefined>(
    undefined,
  );

  async function fetchProgressTotal() {
    const response = await getNormalizedProgress(params.courseID);
    if (response === null) {
      toast({
        title: "Error",
        description: "Failed to fetch progress",
        variant: "destructive",
      });
      return;
    }
    setProgressTotal(response);
  }

  useEffect(() => {
    void fetchProgressTotal();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    void getCourseLearnDataFromAPI(params.courseID).then((data) => {
      setLearnData(data);
      if (data === null) {
        toast({
          title: "Error",
          description: "Failed to fetch data",
          variant: "destructive",
        });
      }
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

  useEffect(() => {
    if (searchParams.get("fetchProgress") === "true") {
      // void getCourseLearnDataFromAPI(params.courseID).then((data) => {
      //   setLearnData(data);
      //   if (data === null) {
      //     toast({
      //       title: "Error",
      //       description: "Failed to fetch data",
      //       variant: "destructive",
      //     })}
      // });
    }
  }, [searchParams]);

  const sidebarImagesItems = learnData?.learn_materials_images.map(
    (element): SidebarItem => {
      return {
        id: element.id,
        name: element.name,
        link: `/course/${params.courseID}/learn/image/${element.id}`,
        learnedChangable: false,
      };
    },
  );
  const sidebarQuizItems = learnData?.learn_materials_quizes.map(
    (element): SidebarItem => {
      return {
        id: element.id,
        name: element.name,
        link: `/course/${params.courseID}/learn/quiz/${element.id}`,
        learnedChangable: false,
      };
    },
  );
  const sidebarVideosItems = learnData?.learn_materials_videos.map(
    (element): SidebarItem => {
      return {
        id: element.id,
        name: element.name,
        link: `/course/${params.courseID}/learn/video/${element.id}`,
        learnedChangable: true,
      };
    },
  );

  const sidebarCategories: SidebarCategory[] = [
    {
      name: "Images",
      sidebarItems: sidebarImagesItems ?? [],
      progressNormalized: progressNormalizedImage,
      setProgressNormalized: setProgressNormalizedImage,
      progressSavable: false,
    },
    {
      name: "Quizes",
      sidebarItems: sidebarQuizItems ?? [],
      progressNormalized: progressNormalizedQuiz,
      setProgressNormalized: setProgressNormalizedQuiz,
      progressSavable: true,
    },
    {
      name: "Videos",
      sidebarItems: sidebarVideosItems ?? [],
      progressNormalized: progressNormalizedVideo,
      setProgressNormalized: setProgresNormalizedVideo,
      progressSavable: true,
    },
  ];

  return (
    <div className="flex h-full w-full justify-center">
      <div className="flex w-full max-w-screen-xl space-x-6">
        <div className="h-full w-4/5 rounded-xl bg-secondary p-8">
          {children}
        </div>
        <div className="h-full w-1/5">
          <Button
            asChild
            className="w-full justify-normal space-x-2 rounded-lg bg-primary px-4 py-2 text-left text-xl font-bold"
          >
            <Link href={`/course/${learnData?.id}/learn`}>
              <Book />
              <p>{learnData?.name}</p>
            </Link>
          </Button>

          <div className="mt-4 space-y-1">
            <p className="text-sm">Course progress</p>
            <div className="flex flex-row items-center space-x-2">
              <p className="text-xs">{progressTotal * 100}%</p>
              <ProgressBar value={progressTotal * 100} />
            </div>
          </div>

          <CourseLearnSidebar
            className="px-5"
            sidebarCategories={sidebarCategories}
            courseID={params.courseID}
            updateProgressTotal={fetchProgressTotal}
          />
        </div>
      </div>
    </div>
  );
}

"use client";

import { useEffect, useMemo, useState } from "react";
import CourseLearnSidebar, {
  type SidebarCategory,
  type SidebarItem,
} from "~/src/components/course/sidebar";
import { type CourseLearn } from "~/src/lib/definitions/course";
import { toast } from '~/src/components/ui/use-toast';
import Link from "next/link";
import { Button } from "~/src/components/ui/button";
import { Book } from "lucide-react";
import {
  getCourseLearnDataFromAPI,
  getProgressNormalized,
  getProgressQuiz,
  getProgressQuizNormalized,
  getProgressVideo,
  getProgressVideoNormalized,
} from "~/src/lib/data/course-learn";
import { Progress as ProgressBar } from "~/src/components/ui/progress";
import { usePathname, useRouter, useSearchParams } from "next/navigation";
import type { Progress as ProgressType } from "~/src/lib/definitions/course-learn";

function showErrorToast(title: string, description: string) {
  toast({
    title: title,
    description: description,
    variant: "destructive",
  });
}

export default function CourseLearnLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: { courseID: string };
}) {
  const router = useRouter();
  const pathName = usePathname();
  const searchParams = useSearchParams();
  const [learnData, setLearnData] = useState<CourseLearn | null | undefined>(
    undefined,
  );
  const [progressTotal, setProgressTotal] = useState<number>(0);
  const [progressNormalizedImage, setProgressNormalizedImage] =
    useState<number>(0);
  const [progressNormalizedQuiz, setProgressNormalizedQuiz] =
    useState<number>(0);
  const [progressNormalizedVideo, setProgressNormalizedVideo] =
    useState<number>(0);
  const [progressQuiz, setProgressQuiz] = useState<ProgressType[] | undefined>(
    undefined,
  );
  const [progressVideo, setProgressVideo] = useState<ProgressType[] | undefined>(
    undefined,
  );
  const [sidebarImagesItems, setSidebarImagesItems] = useState<SidebarItem[]>(
    [],
  );
  const [learnedItems, setLearnedItems] = useState<Record<string, boolean>>({});

  useEffect(() => {
    console.log(learnedItems);
  }, [learnedItems]);

  async function fetchProgressNormalized() {
    const totalprogress = await getProgressNormalized(params.courseID);
    if (totalprogress === null) {
      showErrorToast("Error", "Failed to fetch normalized progress");
    return;
    }
    setProgressTotal(totalprogress);

    const videoProgress = await getProgressVideoNormalized(params.courseID);
    if (videoProgress === null) {
      showErrorToast("Error", "Failed to fetch normalized progress");
      return;
    }
    setProgressNormalizedVideo(videoProgress);

    const quizProgress = await getProgressQuizNormalized(params.courseID);
    if (quizProgress === null) {
      showErrorToast("Error", "Failed to fetch normalized progress");
      return;
    }
    setProgressNormalizedQuiz(quizProgress);
  }

  async function updateLearnedItems() {
    setLearnedItems({
      ...learnedItems,
      ...progressQuiz?.reduce((acc, item) => {
        acc[item.id] = item.is_complete;
        return acc;
      }, {} as Record<string, boolean>),
      ...progressVideo?.reduce((acc, item) => {
        acc[item.id] = item.is_complete;
        return acc;
      }, {} as Record<string, boolean>),
    });
  }

  async function fetchProgressIndividual() {
    const videoProgress = await getProgressVideo(params.courseID);
    if (videoProgress === null) {
      toast({
        title: "Error",
        description: "Failed to fetch video progress",
        variant: "destructive",
      });
      return;
    }
    setProgressVideo(videoProgress);

    const quizProgress = await getProgressQuiz(params.courseID);
    if (quizProgress === null) {
      toast({
        title: "Error",
        description: "Failed to fetch quiz progress",
        variant: "destructive",
      });
      return;
    }
    setProgressQuiz(quizProgress);
  }

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
    void fetchProgressNormalized();
    void fetchProgressIndividual();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    void updateLearnedItems();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [progressQuiz, progressVideo]);

  useEffect(() => {
    if (searchParams.get("fetchProgress") === "true") {
      void fetchProgressNormalized();
      void fetchProgressIndividual();
      router.replace(pathName);
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [pathName, router, searchParams]);


  const sidebarQuizItems = useMemo(() => {
    return learnData?.learn_materials_quizes.map(
      (element): SidebarItem => {
        return {
          id: element.id,
          name: element.name,
          link: `/course/${params.courseID}/learn/quiz/${element.id}`,
          learnedChangable: false,
          learned: learnedItems[element.id] ?? false,
          setLearned: (learned: boolean) => {
            setLearnedItems((prevItems) => ({
              ...prevItems,
              [element.id]: learned,
            }));
          },
        };
      }
    );
  }, [learnData?.learn_materials_quizes, params.courseID, learnedItems]);

  const sidebarVideosItems = useMemo(() => {
    return learnData?.learn_materials_videos.map(
      (element): SidebarItem => {
        return {
          id: element.id,
          name: element.name,
          link: `/course/${params.courseID}/learn/video/${element.id}`,
          learnedChangable: true,
          learned: learnedItems[element.id] ?? false,
          setLearned: (learned: boolean) => {
            setLearnedItems((prevItems) => ({
              ...prevItems,
              [element.id]: learned,
            }));
          },
        };
      }
    );
  }, [learnData?.learn_materials_videos, params.courseID, learnedItems]);

  useEffect(() => {
    if (learnData) {
      setSidebarImagesItems(
        learnData.learn_materials_images.map(
          (element): SidebarItem => {
            return {
              id: element.id,
              name: element.name,
              link: `/course/${params.courseID}/learn/image/${element.id}`,
              learnedChangable: false,
            };
          }
        )
      );
    }
  }, [learnData, params.courseID]);

  const sidebarCategories = useMemo(() => {
    const categories: SidebarCategory[] = [
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
        setProgressNormalized: setProgressNormalizedVideo,
        progressSavable: true,
      },
    ];

    return categories;
  }, [
    sidebarImagesItems,
    sidebarQuizItems,
    sidebarVideosItems,
    progressNormalizedImage,
    progressNormalizedQuiz,
    progressNormalizedVideo,
  ]);

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
            updateProgressTotal={fetchProgressNormalized}
          />
        </div>
      </div>
    </div>
  );
}

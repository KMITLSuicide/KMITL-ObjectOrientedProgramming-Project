"use client";

import { useEffect, useMemo, useState } from "react";
import CourseLearnSidebar, {
  type SidebarCategory,
  type SidebarItem,
} from "~/src/components/course/sidebar-plain";
import type { CourseInfo } from "~/src/lib/definitions/course";
import { toast, useToast } from "~/src/components/ui/use-toast";
import Link from "next/link";
import { Button } from "~/src/components/ui/button";
import { Book, Plus, SquarePen } from "lucide-react";
import { usePathname, useRouter, useSearchParams } from "next/navigation";
import { getSidebarItemsImage, getSidebarItemsQuiz, getSidebarItemsVideo } from "~/src/lib/data/course-learn";
import { getCourseInfoFromAPI } from "~/src/lib/data/course";

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
  const pathName = usePathname();
  const router = useRouter();
  const searchParams = useSearchParams();
  const { toast } = useToast();
  const [courseInfo, setCourseInfo] = useState<CourseInfo | null | undefined>(
    undefined,
  );
  const [sidebarQuizItems, setSidebarQuizItems] = useState<SidebarItem[]>([]);
  const [sidebarVideosItems, setSidebarVideosItems] = useState<SidebarItem[]>([]);
  const [sidebarImagesItems, setSidebarImagesItems] = useState<SidebarItem[]>(
    [],
  );

  async function fetchData(courseID: string) {
    const data = await getCourseInfoFromAPI(courseID);
    setCourseInfo(data);
    if (data === null) {
      toast({
        title: "Error",
        description: "Failed to fetch data",
        variant: "destructive",
      })}
  }

  useEffect(() => {\
    void fetchData(params.courseID);
    console.log(pathName);
    router.replace(pathName);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [params.courseID]);

  useEffect(() => {
    if (searchParams.has("fetch")) {
      // void fetchData(params.courseID);
      window.location.href = pathName;
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [searchParams.get("fetch")]);

  useEffect(() => {
    if (courseInfo === null) {
      toast({
        title: "Access Denied",
        description: "You don't have access to this course.",
        variant: "destructive",
      });
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [courseInfo]);

  useEffect(() => {
    void getCourseInfoFromAPI(params.courseID).then((data) => {
      setCourseInfo(data);
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
    if (courseInfo === null) {
      toast({
        title: "Access Denied",
        description: "You don't have access to this course.",
        variant: "destructive",
      });
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [courseInfo]);

  useEffect(() => {
    const fetchSidebarQuizItems = async () => {
      try {
        const apiSidebarItems = await getSidebarItemsQuiz(params.courseID);
        if (apiSidebarItems === null) {
          showErrorToast("Error", "Failed to fetch quiz items");
          return;
        }
        const items = apiSidebarItems.map((element): SidebarItem => ({
          name: element.name,
          link: `/course/${params.courseID}/edit/quiz/${element.id}`,
        }));
        setSidebarQuizItems(items);
      } catch (error) {
        showErrorToast("Error", "Failed to fetch quiz items");
      }
    };

    void fetchSidebarQuizItems();
  }, [params.courseID]);

  useEffect(() => {
    const fetchSidebarVideosItems = async () => {
      try {
        const apiSidebarItems = await getSidebarItemsVideo(params.courseID);
        if (apiSidebarItems === null) {
          showErrorToast("Error", "Failed to fetch video items");
          return;
        }
        const items = apiSidebarItems.map((element): SidebarItem => ({
          name: element.name,
          link: `/course/${params.courseID}/edit/video/${element.id}`,
        }));
        setSidebarVideosItems(items);
      } catch (error) {
        showErrorToast("Error", "Failed to fetch video items");
      }
    };

    void fetchSidebarVideosItems();
  }, [params.courseID]);

  useEffect(() => {
    const fetchSidebarImagesItems = async () => {
      try {
        const apiSidebarItems = await getSidebarItemsImage(params.courseID);
        if (apiSidebarItems === null) {
          showErrorToast("Error", "Failed to fetch image items");
          return;
        }
        const items = apiSidebarItems.map((element): SidebarItem => ({
          name: element.name,
          link: `/course/${params.courseID}/edit/image/${element.id}`,
        }));
        setSidebarImagesItems(items);
      } catch (error) {
        showErrorToast("Error", "Failed to fetch image items");
      }
    };

    void fetchSidebarImagesItems();
  }, [params.courseID]);

  const sidebarCategories = useMemo(() => {
    const categories: SidebarCategory[] = [
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

    return categories;
  }, [sidebarImagesItems, sidebarQuizItems, sidebarVideosItems]);


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
              <Link href={`/course/${courseInfo?.id}/edit`}>
              <SquarePen />
              <p>
                {courseInfo?.name}
              </p>
              </Link>
            </Button>

            <Button
              asChild
              className=""
              size='icon'
            >
              <Link href={`/course/${courseInfo?.id}/learn`}>
                <Book />
              </Link>
          </Button>
          </div>

          <div className="flex">
            <Button
              asChild
              className="flex-grow justify-normal rounded-lg bg-primary px-4 py-2 text-left text-lg font-semibold space-x-2"
            >
              <Link href={`/course/${courseInfo?.id}/edit/new`} className="flex">
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

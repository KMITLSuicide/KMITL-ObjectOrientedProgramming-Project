import CourseLearnSidebar, { type SidebarCategory, type SidebarItem } from "~/src/components/course/sidebar";
import { ScrollArea } from "~/src/components/ui/scroll-area";
import { getFrontendCourseViewData } from "~/src/lib/data/course";

export default function CourseLearnLayout({
  children,
  params
}: {
  children: React.ReactNode,
  params: { courseID: string }
}) {
  
  const courseData =  getFrontendCourseViewData(params.courseID);
  
  const sidebarImagesItems = courseData.images.map((element): SidebarItem => {
    return({
      name: element.name,
      link: `/course/${params.courseID}/learn/image/${element.id}`
    });
  });
  const sidebarQuizItems = courseData.quizes.map((element): SidebarItem => {
    return({
      name: element.name,
      link: `/course/${params.courseID}/learn/quiz/${element.id}`
    });
  });

  const sidebarCategories: SidebarCategory[] = [{
    name: 'Images',
    sidebarItems: sidebarImagesItems
  }, {
    name: 'Quizes',
    sidebarItems: sidebarQuizItems
  }
]

  return(
    <div className="flex h-full w-full justify-center">
      <div className="flex w-full max-w-screen-xl space-x-6">
        <ScrollArea className="h-full w-4/5 bg-secondary p-6 rounded-xl">
          {children}
        </ScrollArea>
        <div className="w-1/5 h-full">
            <h3 className="text-xl py-2 px-4 bg-primary rounded-lg">
              <b>
                {courseData.name}
              </b>
            </h3>
            <CourseLearnSidebar className="px-5" sidebarCategories={sidebarCategories} />
        </div>
      </div>
    </div>
  )
}
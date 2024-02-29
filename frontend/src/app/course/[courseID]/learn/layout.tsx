import CourseLearnSidebar, { SidebarCategory, SidebarItem } from "~/src/components/course/sidebar";
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
    <div className="flex w-full justify-center">
      <div className="flex w-full max-w-screen-xl space-x-6">
        <div className="w-4/5 bg-secondary p-6 rounded-xl">
          {children}
        </div>
        <div className="w-1/5 p-6">
          <p>im a sidebar</p>
          <CourseLearnSidebar sidebarCategories={sidebarCategories} />
        </div>
      </div>
    </div>
  )
}
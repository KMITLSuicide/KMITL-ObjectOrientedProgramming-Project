import { getFrontendCourseViewData } from "~/src/app/course/[courseID]/page";

export default function CourseLearn({
  params,
}: {
  params: { courseID: string };
}) {
  const courseData = getFrontendCourseViewData(params.courseID);
  return (
    <div className="flex flex-col space-y-2">
      <h4 className="text-lg font-light">Learning</h4>
      <h1 className="text-4xl font-bold">{courseData.name}</h1>
      <p className="text-lg">{courseData.description}</p>
      <p className="text-base font-light">
        Please choose course material on the sidebar.
      </p>
    </div>
  );
}

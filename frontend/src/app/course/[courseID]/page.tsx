export default function CourseLearn({
  params,
}: {
  params: { courseID: string };
}) {
  return (
    <>
      <h1>Course learn</h1>
      <h2>id={params.courseID}</h2>
    </>
  );
}

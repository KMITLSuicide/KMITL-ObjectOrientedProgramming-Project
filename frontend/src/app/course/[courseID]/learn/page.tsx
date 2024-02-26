export default function CourseLearn({
  params,
}: {
  params: { courseID: string };
}) {
  return(
    <>
      <h1>CourseLearn {params.courseID}</h1>
    </>
  )
}
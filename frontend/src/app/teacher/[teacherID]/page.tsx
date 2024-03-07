export default function CoursesByTeacher({
  params,
}: {
  params: { teacherID: string };
}) {


  return(
    <>
      <h1>Teacher ID: {params.teacherID}</h1>
    </>
  );
}

export default function CourseMaterialImage({
  params,
}: {
  params: { courseID: string; imageID: string };
}) {
  return (
    <>
      <h1>Course material image</h1>
      <h2>id={params.courseID}</h2>
      <h2>id={params.imageID}</h2>
    </>
  );
}

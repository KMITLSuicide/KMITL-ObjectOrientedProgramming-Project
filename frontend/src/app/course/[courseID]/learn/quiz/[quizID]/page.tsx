export default function CourseMaterialQuiz({
  params,
}: {
  params: { courseID: string; quizID: string };
}) {
  return (
    <>
      <h1>Course quiz</h1>
      <h2>id={params.courseID}</h2>
      <h2>id={params.quizID}</h2>
    </>
  );
}

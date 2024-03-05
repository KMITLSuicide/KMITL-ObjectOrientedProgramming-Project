export default function CategoryIDPage({
  params,
}: {
  params: { categoryID: string };
}) {
  return(
    <>
      <h1>Category ID: {params.categoryID}</h1>
    </>
  );
}
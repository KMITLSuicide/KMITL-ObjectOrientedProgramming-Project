export default function CourseLearnLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return(
    <div className="flex w-full justify-center">
      <div className="flex w-full max-w-screen-xl space-x-6">
        <div className="w-4/5 bg-secondary p-6 rounded-xl">
          {children}
        </div>
        <div className="w-1/5 p-6">
          <p>im a sidebar</p>
        </div>
      </div>
    </div>
  )
}
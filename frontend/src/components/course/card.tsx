import { type CourseCardData } from "~/src/lib/definitions/course";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "~/src/components/ui/card";
import Image from "next/image";
import { Config } from "~/src/config";
import { useRouter } from "next/navigation";

export function CourseCard({ course }: { course: CourseCardData }) {
  const router = useRouter();

  return(
    <Card
      className="w-full cursor-pointer hover:bg-secondary"
      key={course.id}
      onClick={() => router.push(`/course/${course.id}`)}
    >
      <CardHeader className="">
        <Image className="w-48 mx-auto" alt={`image of course ${course.name}`} src={course.banner_image} width={192} height={144} />
      </CardHeader>
      <CardContent className="space-y-2">
        <CardTitle>{course.name}</CardTitle>
        <CardDescription>{course.description}</CardDescription>
      </CardContent>
      <CardFooter>
        <div className="w-fit flex items-center justify-center rounded-md p-2 outline">{course.price.toLocaleString(Config.locale, {
          style: "currency",
          currency: Config.currency,
          minimumFractionDigits: 0,
        })}</div>
      </CardFooter>
    </Card>
  );
}
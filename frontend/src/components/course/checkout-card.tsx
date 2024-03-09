import { type CourseCardData } from "~/src/lib/definitions/course";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "~/src/components/ui/card";
import Image from "next/image";
import { Config } from "~/src/config";
import Link from "next/link";

export function CourseCardInCheckout({
  course,
  className,
}: {
  course: CourseCardData;
  className?: string;
}) {
  return (
    <Card
      key={course.id}
      className={`w-full cursor-pointer transition-colors hover:bg-secondary ${className}`}
    >
        <Link
          href={`/course/${course.id}`}
          className="flex h-full w-full flex-row items-center pr-4 space-x-2"
        >
          <CardHeader className="flex flex-col p-2">
            <Image
              className="rounded-sm"
              alt={`image of course ${course.name}`}
              src={course.banner_image}
              width={64}
              height={48}
            />
          </CardHeader>
          <CardContent className="flex flex-grow flex-col justify-center space-y-2 p-0">
            <CardTitle className="text-lg">{course.name}</CardTitle>
          </CardContent>
          <CardFooter className="space-x-4 p-0 text-sm">
            <div className="flex w-fit items-center justify-center rounded-md p-2 outline outline-1">
              {course.price.toLocaleString(Config.locale, {
                style: "currency",
                currency: Config.currency,
                minimumFractionDigits: 0,
              })}
            </div>
          </CardFooter>
        </Link>
    </Card>
  );
}

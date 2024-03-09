import { type CourseCardData } from "~/src/lib/definitions/course";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "~/src/components/ui/card";
import Image from "next/image";
import { Config } from "~/src/config";
import Link from "next/link";

export function CourseCard({
  course,
  className,
  customLink,
  showPrice = true,
}: {
  course: CourseCardData;
  className?: string;
  customLink?: string;
  showPrice?: boolean;
}) {
  return (
    <Card
      key={course.id}
      className={`w-full cursor-pointer transition-colors hover:bg-secondary ${className}`}
    >
      <Link
        href={customLink ? customLink : `/course/${course.id}`}
        className="flex h-full w-full flex-col"
      >
        <CardHeader>
          <Image
            className="mx-auto w-48 rounded-md"
            alt={`image of course ${course.name}`}
            src={course.banner_image}
            width={192}
            height={144}
          />
        </CardHeader>
        <CardContent className="flex-grow space-y-2">
          <CardTitle>{course.name}</CardTitle>
          <CardDescription>{course.description}</CardDescription>
        </CardContent>
        {showPrice && (
          <CardFooter>
            <div className="flex w-fit items-center justify-center rounded-md p-2 outline outline-1">
              {course.price.toLocaleString(Config.locale, {
                style: "currency",
                currency: Config.currency,
                minimumFractionDigits: 0,
              })}
            </div>
          </CardFooter>
        )}
      </Link>
    </Card>
  );
}

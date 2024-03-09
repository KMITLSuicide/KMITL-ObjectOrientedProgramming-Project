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
import { Trash } from "lucide-react";
import { Button } from "~/src/components/ui/button";

export function CourseCardInCart({
  course,
  className,
  customLink,
}: {
  course: CourseCardData;
  className?: string;
  customLink?: string;
}) {
  return (
    <Card
      key={course.id}
      className={`w-full cursor-pointer transition-colors hover:bg-secondary ${className}`}
    >
      <Link
        href={customLink ? customLink : `/course/${course.id}`}
        className="flex h-full w-full flex-row items-center pr-6"
      >
        <CardHeader className="flex flex-col">
          <Image
            className="w-32 rounded-sm"
            alt={`image of course ${course.name}`}
            src={course.banner_image}
            width={128}
            height={96}
          />
        </CardHeader>
        <CardContent className="flex flex-col space-y-2 flex-grow justify-center p-0">
          <CardTitle>{course.name}</CardTitle>
          <CardDescription>{course.description}</CardDescription>
        </CardContent>
        <CardFooter className="p-0 space-x-4">
          <div className="flex w-fit items-center justify-center rounded-md p-2 outline outline-1">
            {course.price.toLocaleString(Config.locale, {
              style: "currency",
              currency: Config.currency,
              minimumFractionDigits: 0,
            })}
          </div>

          <Button variant="outline" size="icon" className="hover:bg-destructive">
            <Trash size={24} />
          </Button>
        </CardFooter>
      </Link>
    </Card>
  );
}

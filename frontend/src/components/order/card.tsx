import { type CourseCardData } from "~/src/lib/definitions/course";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "~/src/components/ui/card";
import {
  Form
} from "~/src/components/ui/form";
import Image from "next/image";
import { Config } from "~/src/config";
import Link from "next/link";
import { Trash } from "lucide-react";
import { Button } from "~/src/components/ui/button";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { toast } from "~/src/components/ui/use-toast";
import { deleteCartItem } from "~/src/lib/data/cart";

const FormSchema = z.object({
  id: z.string().min(1),
});

export function OrderCard() {
  const course = {
    course_list: ['course1', 'course2', 'course3'],
    price: 10000,
    address: 'place',
    payment_method: 'visa',
    status: true
  }
  return (
    <Card
      className={`w-full cursor-pointer transition-colors hover:bg-secondary`}
    >
      <div className="flex h-full w-full flex-row items-center pr-6 space-x-2">
        <Link
          href={`/order/orderid`}
          className="flex h-full w-full flex-row items-center"
        >
          <CardHeader className="flex flex-col">
          </CardHeader>
          <CardContent className="flex flex-grow flex-col justify-center space-y-2 p-0">
            <CardTitle>{course.name}</CardTitle>
            <CardDescription>{course.description}</CardDescription>
          </CardContent>
          <CardFooter className="space-x-4 p-0">
            <div className="flex w-fit items-center justify-center rounded-md p-2 outline outline-1">
              {course.price.toLocaleString(Config.locale, {
                style: "currency",
                currency: Config.currency,
                minimumFractionDigits: 0,
              })}
            </div>
          </CardFooter>
        </Link>

        <Form {...form}>
          <form
            onSubmit={form.handleSubmit(onSubmit)}
            className="w-fit space-y-2"
            >
            <Button
              variant="outline"
              size="icon"
              className="hover:bg-destructive"
              type="submit"
              >
              <Trash size={24} />
            </Button>
          </form>
        </Form>
      </div>
    </Card>
  );
}

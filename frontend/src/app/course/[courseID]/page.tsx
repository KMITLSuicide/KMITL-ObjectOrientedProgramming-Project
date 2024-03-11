"use client";

import { ChevronsUpDown } from "lucide-react";
import Image from "next/image";
import Link from "next/link";
import { useEffect, useState } from "react";
import { Button } from "~/src/components/ui/button";
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "~/src/components/ui/collapsible";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "~/src/components/ui/form";
import { toast } from "~/src/components/ui/use-toast";
import { Config } from "~/src/config";
import { createReviews, getCourseInfoFromAPI, getReviews } from "~/src/lib/data/course";
import type { Review, CourseInfo } from "~/src/lib/definitions/course";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { postAddCartItem } from "~/src/lib/data/cart";
import { useRouter } from "next/navigation";
import { ReviewCard } from "~/src/components/course/review-card";
import { Input } from "~/src/components/ui/input";

const BuySchema = z.object({
  id: z.string().min(1),
});

const ReviewSchema = z.object({
  comment: z.string().min(1),
  star: z.coerce.number().int().min(1).max(5),
});

export default function CourseView({
  params,
}: {
  params: { courseID: string };
}) {
  const router = useRouter();
  const [courseContentOpen, setCourseContentOpen] = useState(false);
  const [courseQuizOpen, setCourseQuizOpen] = useState(false);
  const [courseVideoOpen, setCourseVideosOpen] = useState(false);
  const [courseData, setCourseData] = useState<CourseInfo | null>(null);
  const [reviews, setReviews] = useState<Review[] | null>(null);

  const buyForm = useForm<z.infer<typeof BuySchema>>({
    resolver: zodResolver(BuySchema),
    defaultValues: {
      id: params.courseID ?? "",
    },
  });

  async function onSubmitAddToCart(data: z.infer<typeof BuySchema>) {
    const result = await postAddCartItem(data.id);
    if (result === null) {
      toast({
        title: "Error",
        description: "Failed to add item to cart",
        variant: "destructive",
      });
    } else {
      router.push("/cart");
    }
  }

  const reviewForm = useForm<z.infer<typeof ReviewSchema>>({
    resolver: zodResolver(ReviewSchema),
  })

  async function onSubmitReview(data: z.infer<typeof ReviewSchema>) {
    const result = await createReviews(params.courseID, data);
    if (result === null) {
      toast({
        title: "Error",
        description: "Failed to add review",
        variant: "destructive",
      });
    } else {
      setReviews(result);
    }
  }


  useEffect(() => {
    async function fetchData(courseID: string) {
      const apiData = await getCourseInfoFromAPI(courseID);
      setCourseData(apiData);

      if (apiData === null) {
        toast({
          title: "Error",
          description: "Failed to fetch course data",
          variant: "destructive",
        });
      }
    }
    void fetchData(params.courseID);
  }, [params.courseID]);

  useEffect(() => {
    async function fetchData(courseID: string) {
      const apiData = await getReviews(courseID);
      setReviews(apiData);

      if (apiData === null) {
        toast({
          title: "Error",
          description: "Failed to fetch course data",
          variant: "destructive",
        });
      }
    }
    void fetchData(params.courseID);
  }, [params.courseID]);

  return (
    <div className="flex h-full w-full justify-center">
      <div className="flex w-full max-w-screen-xl justify-center">
        <div className="flex w-3/5 flex-col space-y-4">
          <Button
            asChild
            className="w-fit rounded-full bg-secondary p-2 px-4 text-secondary-foreground"
          >
            <Link href={`/category/${courseData?.category_id}`}>
              {courseData?.category_name}
            </Link>
          </Button>

          <h1 className="text-3xl">
            <b>{courseData?.name}</b>
          </h1>

          <p className="text-lg">{courseData?.description}</p>

          <div className="flex w-3/5 flex-col justify-normal space-y-2">
            <h2 className="text-xl">
              <b>In this course:</b>
            </h2>

            <div className="w-max flex flex-col">
              <Collapsible
                open={courseContentOpen}
                onOpenChange={setCourseContentOpen}
                className="w-max space-y-2"
              >
                <div className="flex items-center justify-between space-x-4 rounded-md border p-2 px-4">
                  <h4 className="text-sm font-semibold">Course contents</h4>
                  <CollapsibleTrigger asChild>
                    <Button variant="ghost" size="sm" className="w-9 p-0">
                      <ChevronsUpDown className="h-4 w-4" />
                      <span className="sr-only">Toggle</span>
                    </Button>
                  </CollapsibleTrigger>
                </div>
                <CollapsibleContent className="space-y-2">
                  <ul className="ml-10 list-decimal">
                    {courseData?.materials_images.map((name, index) => {
                      return (
                        <li key={index} className="rounded-md px-2 text-sm">
                          {name}
                        </li>
                      );
                    })}
                  </ul>
                </CollapsibleContent>
              </Collapsible>
            </div>

            <Collapsible
              open={courseQuizOpen}
              onOpenChange={setCourseQuizOpen}
              className="w-max"
            >
              <div className="flex items-center justify-between space-x-4 rounded-md border p-2 px-4">
                <h4 className="text-sm font-semibold">Course quizes</h4>
                <CollapsibleTrigger asChild>
                  <Button variant="ghost" size="sm" className="w-9 p-0">
                    <ChevronsUpDown className="h-4 w-4" />
                    <span className="sr-only">Toggle</span>
                  </Button>
                </CollapsibleTrigger>
              </div>
              <CollapsibleContent className="space-y-2">
                <ul className="ml-10 list-decimal">
                  {courseData?.materials_quizes.map((name, index) => {
                    return (
                      <li key={index} className="rounded-md px-2 text-sm">
                        {name}
                      </li>
                    );
                  })}
                </ul>
              </CollapsibleContent>
            </Collapsible>

            <Collapsible
              open={courseVideoOpen}
              onOpenChange={setCourseVideosOpen}
              className="w-max"
            >
              <div className="flex items-center justify-between space-x-4 rounded-md border p-2 px-4">
                <h4 className="text-sm font-semibold">Course videos</h4>
                <CollapsibleTrigger asChild>
                  <Button variant="ghost" size="sm" className="w-9 p-0">
                    <ChevronsUpDown className="h-4 w-4" />
                    <span className="sr-only">Toggle</span>
                  </Button>
                </CollapsibleTrigger>
              </div>
              <CollapsibleContent className="space-y-2">
                <ul className="ml-10 list-decimal">
                  {courseData?.materials_videos.map((name, index) => {
                    return (
                      <li key={index} className="rounded-md px-2 text-sm">
                        {name}
                      </li>
                    );
                  })}
                </ul>
              </CollapsibleContent>
            </Collapsible>
          </div>

          <div className="flex w-3/5 flex-col justify-normal space-y-2">
            <h2 className="text-xl font-bold">
              Reviews
            </h2>
            <div>
              {reviews?.map((review, index) => {
                return (
                  <ReviewCard review={review} key={index} />
                );
              })}
            </div>
            <div>
              <h2 className="text-xl font-bold mb-2">
              Leave your review
              </h2>
              <Form {...reviewForm}>
                <form onSubmit={reviewForm.handleSubmit(onSubmitReview)} className="w-full space-y-4">
                  <div className="flex flex-row space-x-2">
                    <FormField
                      control={reviewForm.control}
                      name="comment"
                      render={({ field }) => (
                        <FormItem className="w-full">
                          <FormLabel>Comment</FormLabel>
                          <FormControl>
                            <Input placeholder="Comment..." {...field} />
                          </FormControl>
                          <FormMessage />
                        </FormItem>
                      )}
                    />

                    <FormField
                      control={reviewForm.control}
                      name="star"
                      render={({ field }) => (
                        <FormItem className="w-24">
                          <FormLabel>Stars</FormLabel>
                          <FormControl>
                            <Input placeholder="5" {...field} type="number" />
                          </FormControl>
                          <FormMessage />
                        </FormItem>
                      )}
                    />
                  </div>
                  <Button variant="default" type="submit">Leave a review</Button>
                </form>
              </Form>
            </div>
          </div>

        </div>
        <div className="flex h-fit w-2/5 rounded-lg bg-secondary p-4">
          <div className="flex flex-col items-center justify-center space-y-4">
            <Image
              className="rounded-md"
              src={courseData?.banner_image ?? "/notexture.png"}
              alt="course hero image"
              width={1920}
              height={1080}
              sizes="100%"
            />

            <div className="flex items-center justify-center rounded-md p-4 text-xl outline">
              <h3 className="text-2xl">
                <b>
                  {courseData?.price.toLocaleString(Config.locale, {
                    style: "currency",
                    currency: Config.currency,
                    minimumFractionDigits: 0,
                  })}
                </b>
              </h3>
            </div>

            <div className="flex w-full justify-center space-x-6">
              <Form {...buyForm}>
                <form
                  onSubmit={buyForm.handleSubmit(onSubmitAddToCart)}
                  className="w-fit space-y-2"
                >
                  <Button variant="link" type="submit">
                    Add to cart
                  </Button>
                </form>
              </Form>

              <Button variant="default" type="submit" asChild>
                <Link href={`/cart/checkout?buynow=${params.courseID}`}>
                  Buy now!
                </Link>
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

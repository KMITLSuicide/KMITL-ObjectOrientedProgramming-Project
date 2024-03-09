'use client';

import { useEffect, useState } from "react";
import { CourseCardInCart } from "~/src/components/course/cart-card";
import { Button } from "~/src/components/ui/button";
import { toast } from "~/src/components/ui/use-toast";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "~/src/components/ui/form";
import { Config } from "~/src/config";
import { getMyCart } from "~/src/lib/data/cart";
import type { CourseCardData } from "~/src/lib/definitions/course";
import { z } from "zod";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { Input } from "~/src/components/ui/input";

const FormSchema = z.object({
  couponCode: z.string().min(1),
})

export default function Cart() {
  const [cardsData, setCardsData] = useState<CourseCardData[] | null | undefined>(undefined);
  const [totalPrice, setTotalPrice] = useState<number | undefined>(undefined);
  useEffect(() => {
    async function fetchData() {
      const apiData = await getMyCart();
      setCardsData(apiData);
      if (apiData === null) {
        toast({
          title: "Error",
          description: "Failed to fetch my cart",
          variant: "destructive",
        });
      }
    }
    void fetchData();
  }, []);

  useEffect(() => {
    if (cardsData) {
      let total = 0;
      cardsData.forEach((course) => {
        total += course.price;
      });
      setTotalPrice(total);
    }
  }, [cardsData]);

  const form = useForm<z.infer<typeof FormSchema>>({
    resolver: zodResolver(FormSchema),
    defaultValues: {
      couponCode: "",
    },
  })

  function onSubmit(data: z.infer<typeof FormSchema>) {
    toast({
      title: "You submitted the following values:",
      description: (
        <pre className="mt-2 w-[340px] rounded-md bg-slate-950 p-4">
          <code className="text-white">{JSON.stringify(data, null, 2)}</code>
        </pre>
      ),
    })
  }

  return (
    <div className="flex w-full justify-center">
      <div className="flex flex-col w-full max-w-screen-lg space-y-4">
        <h1 className="text-3xl font-bold ml-6">Cart</h1>

        <div className="flex flex-row w-full space-x-6">

          <div className="w-full grid gap-4">
            {cardsData?.map((course) => {
              return (<CourseCardInCart key={course.id} course={course} />);
            })}
          </div>

          <div className="w-2/5 h-fit bg-secondary rounded-lg p-6 space-y-4">
            <div>
              <h2 className="text-sm">Total</h2>
              <p className="text-4xl font-bold">
                {totalPrice?.toLocaleString(Config.locale, {
                  style: "currency",
                  currency: Config.currency,
                  minimumFractionDigits: 0,
                })}
            </p>
            </div>
            <Button className="w-full">Checkout</Button>
            <hr className="h-px border-0 bg-muted-foreground" />

            <Form {...form}>
              <form onSubmit={form.handleSubmit(onSubmit)} className="w-full space-y-2">
                <FormField
                  control={form.control}
                  name="couponCode"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Coupon code</FormLabel>
                      <FormControl>
                        <Input placeholder="TAJDANG888" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <Button type="submit" className="w-full">Submit</Button>
              </form>
            </Form>
          </div>
        </div>


      </div>
    </div>
  );
}
"use client";

import { useEffect, useState } from "react";
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
import { cartCheckout, getMyCart, getPaymentMethods } from "~/src/lib/data/cart";
import type { CourseCardData } from "~/src/lib/definitions/course";
import { z } from "zod";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { Input } from "~/src/components/ui/input";
import { ScrollArea } from "~/src/components/ui/scroll-area";
import { CourseCardInCheckout } from "~/src/components/course/checkout-card";
import { RadioGroup, RadioGroupItem } from "~/src/components/ui/radio-group";
import type { PaymentMethodWithID } from "~/src/lib/definitions/cart";
import { v4 as uuidv4 } from "uuid";
import { Checkbox } from "~/src/components/ui/checkbox";
import { useRouter } from "next/navigation";

const FormSchema = z.object({
  billingCountry: z.string().min(1),
  paid: z.boolean(),
  paymentMethod: z.string().min(1),
});

export default function CheckoutPage() {
  const router = useRouter();
  const [cardsData, setCardsData] = useState<
    CourseCardData[] | null | undefined
  >(undefined);
  const [totalPrice, setTotalPrice] = useState<number | undefined>(undefined);
  const [paymentMethods, setPaymentMethods] = useState<PaymentMethodWithID[]>([]);

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

  useEffect(() => {
    void fetchData();
  }, []);

  useEffect(() => {
    void getPaymentMethods().then((response) => {
      if (response === null) {
        toast({
          title: "Error",
          description: "Failed to fetch payment methods",
          variant: "destructive",
        });
      }
      const paymentMethodWithID = response?.map((method) => {
        return { ...method, id: uuidv4() };
      });
      setPaymentMethods(paymentMethodWithID ?? []);
    });
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
  });

  function onSubmit(data: z.infer<typeof FormSchema>) {
    // toast({
    //   title: "You submitted the following values:",
    //   description: (
    //     <pre className="mt-2 w-[340px] rounded-md bg-slate-950 p-4">
    //       <code className="text-white">{JSON.stringify(data, null, 2)}</code>
    //     </pre>
    //   ),
    // });
    void cartCheckout({
      address: data.billingCountry,
      is_paid: data.paid,
      payment_method: data.paymentMethod,
    }).then((response) => {
      if (response === null) {
        toast({
          title: "Error",
          description: "Failed to checkout",
          variant: "destructive",
        });
      } else {
        toast({
          title: "Success",
          description: "Checkout successful",
        });
        router.push(`/account/order/${response.id}`)
      }
    });
  }

  return (
    <div className="flex h-full w-full justify-center">
      <div className="flex h-full w-full max-w-screen-lg flex-col space-y-4">
        <div>
          <h1 className="text-3xl font-bold">Checkout</h1>
          <p className="text-base">Items: {cardsData?.length ?? 0}</p>
        </div>

        <Form {...form}>
          <form
            onSubmit={form.handleSubmit(onSubmit)}
            className="w-full space-y-6"
          >
            <div className="flex h-full w-full flex-row space-x-6">
              <div className="flex h-full w-full flex-col space-y-6">
                <FormField
                  control={form.control}
                  name="billingCountry"
                  render={({ field }) => (
                    <FormItem>
                      <h2 className="text-xl font-bold">Billing country</h2>

                      <FormControl>
                        <Input placeholder={String(Config.countryName)} {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <FormField
                  control={form.control}
                  name="paymentMethod"
                  render={({ field }) => (
                    <FormItem className="space-y-3">
                      <h2 className="text-xl font-bold">Payment Method</h2>
                      <FormControl>
                        <RadioGroup
                          onValueChange={field.onChange}
                          defaultValue={field.value}
                          className="flex flex-col space-y-1"
                        >
                          {paymentMethods.map((method) => {
                            return (
                              <FormItem
                                key={method.id}
                                className="flex items-center space-x-3 space-y-0"
                              >
                                <FormControl>
                                  <RadioGroupItem value={method.name} />
                                </FormControl>
                                <FormLabel className="font-normal">
                                  {method.name}
                                </FormLabel>
                              </FormItem>
                            );
                          })}
                        </RadioGroup>
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <FormField
                  control={form.control}
                  name="paid"
                  render={({ field }) => (
                    <FormItem className="flex flex-row items-start space-x-3 space-y-0 ">
                      <FormControl>
                        <Checkbox
                          checked={field.value}
                          onCheckedChange={field.onChange}
                        />
                      </FormControl>
                      <div className="space-y-1 leading-none">
                        <FormLabel>
                          I have paid.
                        </FormLabel>
                      </div>
                    </FormItem>
                  )}
                />
                <div></div>
                <div className="h-full">
                  <h2 className="mb-2 text-xl font-bold">Your order</h2>
                  <ScrollArea className="grid h-[90%] w-full">
                    {cardsData?.map((course) => {
                      return (
                        <CourseCardInCheckout
                          key={course.id}
                          course={course}
                          className="my-1"
                        />
                      );
                    })}
                  </ScrollArea>
                </div>
              </div>

              <div className="h-fit w-2/5 space-y-4 rounded-lg bg-secondary p-6">
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
                <Button className="w-full" type="submit">
                  Pay
                </Button>
              </div>
            </div>
          </form>
        </Form>
      </div>
    </div>
  );
}

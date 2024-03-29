'use client';
export const runtime = 'edge';

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { Button } from "~/src/components/ui/button";
import { toast } from "~/src/components/ui/use-toast";
import { Config } from "~/src/config";
import { getOrder, setOrderPaid } from "~/src/lib/data/order";
import type { Order } from "~/src/lib/definitions/order";

export default function ViewOrder({
  params
  } : {
  params: { orderID: string }
}) {
  const router = useRouter();
  const [order, setOrder] = useState<Order | null | undefined>(undefined);
  const [date, setDate] = useState<Date | null>(null);
  useEffect(() => {
    void getOrder(params.orderID).then((data) => {
      setOrder(data);
      if (data === null) {
        toast({
          title: "Error",
          description: "Failed to fetch data",
          variant: "destructive",
        });
      }
      if (data?.time_stamp) {
        setDate(new Date(data?.time_stamp * 1000));
      }
    });
  }, [params.orderID]);

  return (
    <div className="flex w-full justify-center">
      <div className="w-full max-w-screen-lg space-y-4">
        <h1 className="text-3xl font-bold">Your Order</h1>
        <div>
          <h3 className="text-base">Placed on: {date?.toLocaleString()}</h3>
          <p className="text-sm text-muted-foreground">ID: {order?.id}</p>
        </div>
        <div>
          <h2 className="text-xl font-bold">In this order:</h2>
          <ul className="ml-4 list-disc">
            {order?.course_list_name.map((courseName, i) => {
              return (
                <li key={i} className="list">
                  {courseName}
                </li>
              );
            })}
          </ul>
        </div>
        <div className="space-y-1">
          <h2 className="text-xl font-bold">Your payment:</h2>
          <div className="flex flex-row items-center space-x-2">
            {order?.status ? (
              <p className="py-2 px-4 text-sm rounded-full bg-primary text-primary-foreground w-fit">Paid</p>
              ) : (
                <p className="py-2 px-4 text-sm rounded-full bg-destructive text-destructive-foreground w-fit">Not paid</p>
                )}
            <p>{order?.price.toLocaleString(Config.locale, {
                style: "currency",
                currency: Config.currency,
                minimumFractionDigits: 0,
              })}</p>
          </div>
          {order?.status == false && (
            <div>
              <Button variant="secondary" onClick={() => {
                void setOrderPaid(order?.id).then((data) => {
                  setOrder(data);
                  if (data === null) {
                    toast({
                      title: "Error",
                      description: "Failed to fetch data",
                      variant: "destructive",
                    });
                  } else {
                    toast({
                      title: "Success",
                      description: "Payment success",
                    });
                    router.push(`/account/order/${order?.id}`)
                  }
                });
              }}>
                Pay remaining
              </Button>
            </div>
          )}
          <div>
            <p>via {order?.payment_method}</p>
          </div>
          <h3 className="text-lg font-semibold">Billing address:</h3>
          <p>{order?.address}</p>
        </div>
      </div>
    </div>
  );
}

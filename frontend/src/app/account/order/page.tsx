'use client';

import { useEffect, useState } from "react";
import { OrderCard } from "~/src/components/order/card";
import { toast } from "~/src/components/ui/use-toast";
import { getAllOrders } from "~/src/lib/data/order";
import type { AllOrderItem } from "~/src/lib/definitions/order";

export default function OrderPage() {
  const [order, setOrder] = useState<AllOrderItem[] | null | undefined>(undefined);
  useEffect(() => {
    void getAllOrders().then((data) => {
      setOrder(data);
      if (data === null) {
        toast({
          title: "Error",
          description: "Failed to fetch data",
          variant: "destructive",
        });
      }
    });
  }, []);

  return (
    <div className="flex w-full justify-center">
      <div className="w-full max-w-screen-lg space-y-4">
        <h1 className="text-3xl font-bold">My Orders</h1>
        <div className="space-y-2 mx-4">
          {
            order?.map((order) => (
            <OrderCard order={order} key={order.id} />))
          }
        </div>
      </div>
    </div>
  );
}
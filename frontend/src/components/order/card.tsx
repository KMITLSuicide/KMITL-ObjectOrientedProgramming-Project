import {
  Card,
  CardContent,
  CardFooter,
  CardTitle,
} from "~/src/components/ui/card";
import { Config } from "~/src/config";
import Link from "next/link";
import type { AllOrderItem } from "~/src/lib/definitions/order";

export function OrderCard({
  order
}: {
  order: AllOrderItem;
}) {
  return (
    <Card
      className={`w-full cursor-pointer transition-colors hover:bg-secondary`}
    >
      <div className="flex h-full w-full flex-row items-center px-6 py-2 space-x-2">
        <Link
          href={`/account/order/${order.id}`}
          className="flex h-full w-full flex-row items-center"
        >
          <CardContent className="flex flex-grow flex-col justify-center space-y-2 p-0">
            <CardTitle className="text-base">{order.id}</CardTitle>
          </CardContent>
          <CardFooter className="space-x-4 p-0">
            <div className="flex w-fit items-center justify-center rounded-md p-2 outline outline-1">
              {order.price.toLocaleString(Config.locale, {
                style: "currency",
                currency: Config.currency,
                minimumFractionDigits: 0,
              })}
            </div>
          </CardFooter>
        </Link>
      </div>
    </Card>
  );
}

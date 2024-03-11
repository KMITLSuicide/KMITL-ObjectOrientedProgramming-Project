import { Config } from "~/src/config";

export default function ViewOrder({ params }: { params: { orderID: string } }) {
  const course = {
    id: "orderid_ahdsflhskfjhklsdhfjsdhl",
    course_list: ["course1", "course2", "course3"],
    price: 10000,
    address: "place",
    payment_method: "visa",
    status: true,
  };

  return (
    <div className="flex w-full justify-center">
      <div className="w-full max-w-screen-lg space-y-4">
        <h1 className="text-3xl font-bold">Your Order</h1>
        <p className="text-sm text-muted-foreground">{course.id}</p>
        <div>
          <h2 className="text-xl font-bold">In this order:</h2>
          <ul className="ml-4 list-disc">
            {course.course_list.map((courseName, i) => {
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
            {course.status ? (
              <p className="py-2 px-4 text-sm rounded-full bg-primary text-primary-foreground w-fit">Paid</p>
              ) : (
                <p className="py-2 px-4 text-sm rounded-full bg-destructive text-destructive-foreground w-fit">Not paid</p>
                )}
            <p>{course.price.toLocaleString(Config.locale, {
                style: "currency",
                currency: Config.currency,
                minimumFractionDigits: 0,
              })}</p>
          </div>
          <div>
            <p>Paid via {course.payment_method}</p>
          </div>
          <h3 className="text-lg font-semibold">Billing address:</h3>
          <p>{course.address}</p>
        </div>
      </div>
    </div>
  );
}

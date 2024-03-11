export default function OrderPage() {
  return (
    <div>
      <h1>My Orders</h1>
      <OrderList orders={data.orders} />
    </div>
  );
}
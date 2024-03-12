import api from "~/src/lib/data/api";
import type { AllOrderItem, Order } from "~/src/lib/definitions/order";

export async function getAllOrders() {
  try {
    const response = await api.get<AllOrderItem[]>("/user/orders");

    if (response.status == 200) {
      return response.data;
    } else {
      return null;
    }
  } catch (error) {
    console.error(error);
    return null;
  }
}

export async function getOrder(orderID: string) {
  try {
    const response = await api.get<Order>(`/user/order/${orderID}`);

    if (response.status == 200) {
      return response.data;
    } else {
      return null;
    }
  } catch (error) {
    console.error(error);
    return null;
  }
}

export async function setOrderPaid(orderID: string) {
  try {
    const response = await api.put<Order>(`/user/order/${orderID}`);

    if (response.status == 200) {
      return response.data;
    } else {
      return null;
    }
  } catch (error) {
    console.error(error);
    return null;
  }
}
import api from "~/src/lib/data/api";
import type { BuyPostData, PaymentMethod } from "~/src/lib/definitions/cart";
import type { CourseCardData } from "~/src/lib/definitions/course";
import { Order } from "~/src/lib/definitions/order";

export async function getMyCart() {
  try {
    const response = await api.get<CourseCardData[]>("/user/cart");

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

export async function deleteCartItem(course_id: string) {
  try {
    const response = await api.delete<CourseCardData[]>(`/user/cart?course_id=${course_id}`);

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

export async function postAddCartItem(course_id: string) {
  try {
    const response = await api.post<CourseCardData[]>(`/user/cart?course_id=${course_id}`);

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

export async function getPaymentMethods() {
  try {
    const response = await api.get<PaymentMethod[]>("/payment_method");

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

export async function cartCheckout(data: BuyPostData) {
  try {
    const response = await api.post<Order>("/user/buy/cart", data);

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

export async function buyNow(data: BuyPostData, courseID: string) {
  try {
    const response = await api.post<Order>(`/user/buy/now/${courseID}`, data);

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
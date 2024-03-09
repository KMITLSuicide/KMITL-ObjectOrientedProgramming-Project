import api from "~/src/lib/data/api";
import { type CourseCardData } from "~/src/lib/definitions/course";

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
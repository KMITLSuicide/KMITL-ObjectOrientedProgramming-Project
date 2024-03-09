import api from "~/src/lib/data/api";
import { type CourseCardData } from "~/src/lib/definitions/course";

export async function getMyCart() {
  try {
    const response = await api.get<CourseCardData[]>("/user/cart?course_id=f61e30e3-6bdb-41bc-9c24-09034d326548");

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

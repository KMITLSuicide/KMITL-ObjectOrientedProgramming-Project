import api from "~/src/lib/data/api";
import { type CourseCategory } from "~/src/lib/definitions/course";

export async function getCategoryDataFromAPI() {
  try {
    const response = await api.get<CourseCategory[]>('/category');

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

export async function getCategoryDataWithIDFromAPI(categoryID: string) {
  try {
    const response = await api.get<CourseCategory>(`/category/${categoryID}`);

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
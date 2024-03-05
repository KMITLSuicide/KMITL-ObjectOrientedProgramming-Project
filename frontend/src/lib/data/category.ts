import api from "~/src/lib/data/api";
import { CourseData } from "./course";
export interface CategoryData {
  _CourseCategory__id: string;
  _CourseCategory__name: string;
  _CourseCategory_courses: CourseData[];
};



export async function getCategoryDataFromAPI() {
  try {
    const response = await api.get<CategoryData[]>('/category');


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
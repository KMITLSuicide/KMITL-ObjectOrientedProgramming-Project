import api from "~/src/lib/data/api";
import { type CourseCardData } from "~/src/lib/definitions/course";

export async function getReccommendedCourses() {
  try {
    const response = await api.get<CourseCardData[]>(`/course/homepage/random_course`);

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

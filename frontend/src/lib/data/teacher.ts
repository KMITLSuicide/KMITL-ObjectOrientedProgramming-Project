import api from "~/src/lib/data/api";
import { type CourseCardDataWithLabel} from "~/src/lib/definitions/course";

export async function getCoursesByTeachers(teacherID: string) {
  try {
    const response = await api.get<CourseCardDataWithLabel>(`/teacher/${teacherID}/course`);

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
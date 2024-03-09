import api from "~/src/lib/data/api";
import { type CourseCardData } from "~/src/lib/definitions/course";

export async function getMyLearnings() {
  try {
    const response = await api.get<CourseCardData[]>("/user/learnings");

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

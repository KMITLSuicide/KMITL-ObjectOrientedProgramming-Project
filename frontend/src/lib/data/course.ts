import type {
  CourseInfo,
  Course,
  CourseLearn,
  CourseCreatePostData,
  CourseCardData,
} from "~/src/lib/definitions/course";
import api from "~/src/lib/data/api";

export async function getCourseDataFromAPI() {
  try {
    const response = await api.get<Course[]>("/course");

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

export async function getCourseInfoFromAPI(courseID: string) {
  try {
    const response = await api.get<CourseInfo>(`/course/${courseID}`);

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

export async function getCourseLearnDataFromAPI(courseID: string) {
  try {
    const response = await api.get<CourseLearn>(`/course/${courseID}/learn`);

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

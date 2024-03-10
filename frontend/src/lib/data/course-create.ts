import api from "~/src/lib/data/api";
import type { CourseCardData } from "~/src/lib/definitions/course";
import type { CourseCreatePostData, CreateMaterialImagePostData, CreateMaterialQuizPostData, CreateMaterialVideoPostData } from "~/src/lib/definitions/course-create";

export async function createCourseToAPI(data: CourseCreatePostData) {
  try {
    const response = await api.post<CourseCardData>("/course", data);

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

export async function createMaterialImage(data: CreateMaterialImagePostData, courseID: string) {
  try {
    const response = await api.post<string>(`/course/${courseID}/image`, data);

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

export async function createMaterialVideo(data: CreateMaterialVideoPostData, courseID: string) {
  try {
    const response = await api.post<string>(`/course/${courseID}/video`, data);

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

export async function createMaterialQuiz(data: CreateMaterialQuizPostData, courseID: string) {
  try {
    const response = await api.post<string>(`/course/${courseID}/quiz`, data);

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
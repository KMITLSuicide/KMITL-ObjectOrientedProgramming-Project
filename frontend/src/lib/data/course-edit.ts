import api from "~/src/lib/data/api";
import type { CourseCreatePostData } from "~/src/lib/definitions/course";
import type { EditQuestionPostData, MaterialImageEditPostData, MaterialVideoEditPostData } from "~/src/lib/definitions/course-edit";

export async function createQuestion(courseID: string, quizID: string, data: EditQuestionPostData) {
  try {
    const response = await api.post<string>(`/course/${courseID}/quiz/${quizID}/question`, data);

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

export async function editQuestion(courseID: string, quizID: string, questionID: string, data: EditQuestionPostData) {
  try {
    const response = await api.put<string>(`/course/${courseID}/quiz/${quizID}/question/${questionID}`, data);

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

export async function editCourseInfo(courseID: string, data: CourseCreatePostData) {
  try {
    const response = await api.put<string>(`/course/${courseID}`, data);

    if (response.status == 200) {
      return true;
    } else {
      return false;
    }
  } catch (error) {
    console.error(error);
    return false;
  }
}

export async function editMaterialImage(courseID: string, imageID: string, data: MaterialImageEditPostData) {
  try {
    const response = await api.put<string>(`/course/${courseID}/image/${imageID}`, data);

    if (response.status == 200) {
      return true;
    } else {
      return false;
    }
  } catch (error) {
    console.error(error);
    return false;
  }
}

export async function editMaterialVideo(courseID: string, videoID: string, data: MaterialVideoEditPostData) {
  try {
    const response = await api.put<string>(`/course/${courseID}/video/${videoID}`, data);

    if (response.status == 200) {
      return true;
    } else {
      return false;
    }
  } catch (error) {
    console.error(error);
    return false;
  }
}

export async function deleteCourse(courseID: string) {
  try {
    const response = await api.delete<string>(`/course/${courseID}`);

    if (response.status == 200) {
      return true;
    } else {
      return false;
    }
  } catch (error) {
    console.error(error);
    return false;
  }
}
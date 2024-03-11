import api from "~/src/lib/data/api";
import type { CourseLearn } from "~/src/lib/definitions/course";
import type { CompleteQuizResponse, CompleteVideoPostData } from "~/src/lib/definitions/course-learn";

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

export async function completeQuiz(courseID: string, quizID: string, data: { "ids": string[] }) {
  try {
    const response = await api.put<CompleteQuizResponse>(`/user/progress/${courseID}/quiz/${quizID}`, data);
    console.log(response);

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

export async function completeVideo(courseID: string, data: CompleteVideoPostData) {
  try {
    const response = await api.put<number>(`/user/progress/${courseID}/video`, data);

    if (response.status == 200) {
      return response.data;
    } else {
      return false;
    }
  } catch (error) {
    console.error(error);
    return false;
  }
}
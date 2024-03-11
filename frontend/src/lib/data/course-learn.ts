import api from "~/src/lib/data/api";
import type { CourseLearn } from "~/src/lib/definitions/course";
import type { CompleteQuizResponse } from "~/src/lib/definitions/course-learn";

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
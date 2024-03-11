import api from "~/src/lib/data/api";
import type { EditQuestionPostData } from "~/src/lib/definitions/course-edit";

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
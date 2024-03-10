import type {
  CourseInfo,
  Course,
  CourseLearn,
  CourseCreatePostData,
  CourseCardData,
  Review,
  PostReviewData,
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

export async function getReviews(courseID: string) {
  try {
    const response = await api.get<Review[]>(`/course/${courseID}/review`);

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

export async function createReviews(courseID: string, data: PostReviewData) {
  try {
    const response = await api.post<Review[]>(`/course/${courseID}/create_review`, data);

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
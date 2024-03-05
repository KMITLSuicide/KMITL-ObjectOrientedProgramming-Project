import { User } from "./user";
interface CourseQuestion {
  _QuizQuestion__question: string;
  _QuizQuestion__correct: string;
}
interface CourseMaterial {
  _CourseMaterial__id: string;
  _CourseMaterial__name: string;
  _CourseMaterial__name: string;
}

interface CourseMaterialImage extends CourseMaterial {
  _CourseMaterialImage__url: string;
}

export interface CourseMaterialQuiz extends CourseMaterial {
  _CourseMaterialQuiz__questions: CourseQuestion[];
}
export interface CourseMaterialVideo extends CourseMaterial{
  _CourseMaterialImage__url: string;
}
interface CourseReview
{
  _CourseReview__reviewer: User;
  _CourseReview__star: number;
  _CourseReview__comment: string
}
export interface Course {
  _Course__id: string;
  _Course__name: string;
  _Course__description: string;
  _Course__price: number;
  _Course__quizes: CourseMaterialQuiz[];
  _Course__images: CourseMaterialImage[];
  _Course__reviews : CourseReview[];
  _Course__latest_video : null | CourseMaterialVideo;
}

interface CourseCategory {
  _CourseCategory__id: string;
  _CourseCategory__name: string;
  _CourseCategory__courses: Course[];
}
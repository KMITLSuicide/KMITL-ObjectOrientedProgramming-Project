import { User } from "./user";
interface CourseQuestion {
  question: string;
  correct: string;
}
interface CourseMaterial {
  id: string;
  name: string;
  description: string;
}

interface CourseMaterialImage extends CourseMaterial {
  url: string;
}

interface CourseMaterialQuiz extends CourseMaterial {
  questions: CourseQuestion[];
}
interface CourseMaterialVideo extends CourseMaterial{

}
interface CourseReview
{
  _CourseReview__reviewer: User;
  _CourseReview__star: number;
  _CourseReview__comment: string
}
interface CourseMaterialVideo{}
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
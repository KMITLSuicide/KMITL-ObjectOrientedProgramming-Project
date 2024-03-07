export interface CourseQuestion {
  _QuizQuestion__question: string;
  _QuizQuestion__correct: string;
}
export interface CourseMaterial {
  _CourseMaterial__id: string;
  _CourseMaterial__name: string;
  _CourseMaterial__name: string;
}

export interface CourseMaterialImage extends CourseMaterial {
  _CourseMaterialImage__url: string;
}

export interface CourseMaterialQuiz extends CourseMaterial {
  _CourseMaterialQuiz__questions: CourseQuestion[];
}
export interface CourseMaterialVideo extends CourseMaterial{
  _CourseMaterialImage__url: string;
}
export interface CourseReview
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

export interface CourseCategory {
  _CourseCategory__id: string;
  _CourseCategory__name: string;
  _CourseCategory__courses: Course[];
}

interface CourseCardData {
  id: string;
  name: string;
  description: string;
  price: number;
  rating: number;
  banner_image: string;
}

interface CourseInfo {
  id: string;
  name: string;
  description: string;
  category_id: string;
  category_name: string;
  price: number;
  rating: number;
  banner_image: string;
  materials_images: string[];
  materials_quizes: string[];
  materials_videos: string[];
}
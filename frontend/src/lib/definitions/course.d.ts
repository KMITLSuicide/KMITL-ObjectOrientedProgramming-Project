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
export interface CourseMaterialVideo extends CourseMaterial {
  _CourseMaterialImage__url: string;
}
export interface CourseReview {
  _CourseReview__reviewer: User;
  _CourseReview__star: number;
  _CourseReview__comment: string;
}
export interface Course {
  _Course__id: string;
  _Course__name: string;
  _Course__description: string;
  _Course__price: number;
  _Course__quizes: CourseMaterialQuiz[];
  _Course__images: CourseMaterialImage[];
  _Course__reviews: CourseReview[];
  _Course__latest_video: null | CourseMaterialVideo;
}

export interface CourseCategory {
  _CourseCategory__id: string;
  _CourseCategory__name: string;
  _CourseCategory__courses: Course[];
}

export interface CourseCardData {
  id: string;
  name: string;
  description: string;
  price: number;
  rating: number;
  banner_image: string;
}

export interface CourseCardDataWithLabel {
  id: string;
  label: string;
  cards: CourseCardData[];
}

export interface CourseInfo {
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

export interface CourseLearnMaterial {
  id: string;
  name: string;
  description: string;
}

export interface CourseLearnMaterialQuizQuestions {
  id: string;
  question: string;
}

export interface CourseLearnMaterialQuizQuestionsWithKey extends CourseLearnMaterialQuizQuestions {
  correct: boolean;
}

export interface CourseLearnMaterialQuiz extends CourseLearnMaterial {
  questions: CourseLearnMaterialQuizQuestions[];
}

export interface CourseLearnMaterialQuizWithKey extends CourseLearnMaterial {
  questions: CourseLearnMaterialQuizQuestionsWithKey[];
}

export interface CourseLearnMaterialImage extends CourseLearnMaterial {
  url: string;
}

export interface CourseLearnMaterialVideo extends CourseLearnMaterial {
  url: string;
}

export interface CourseLearn extends CourseInfo {
  learn_materials_quizes: CourseLearnMaterialQuiz[];
  learn_materials_images: CourseLearnMaterialImage[];
  learn_materials_videos: CourseLearnMaterialVideo[];
}

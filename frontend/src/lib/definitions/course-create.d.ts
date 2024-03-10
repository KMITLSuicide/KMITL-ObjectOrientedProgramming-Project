export interface CourseCreatePostData {
  name: string;
  description: string;
  price: number;
  category_id: string;
}

export interface CreateMaterialBasePostData {
  name: string;
  description: string;
}

export interface CreateMaterialImagePostData extends CreateMaterialBasePostData {
  url: string
}

export interface CreateMaterialVideoPostData extends CreateMaterialBasePostData {
  url: string
}

export interface CreateMaterialQuizPostData extends CreateMaterialBasePostData {
  questions: {
    question: string;
    correct: boolean;
  }[];
}
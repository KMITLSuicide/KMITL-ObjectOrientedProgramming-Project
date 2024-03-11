export interface CompleteQuizResponse{
  "result": boolean,
  "message": string,
  "progress_normalized": number
}

export interface CompleteVideoPostData{
  "id": string,
  "is_complete": boolean
}

export interface VideoInfo {
  id: string;
  name: string;
  description: string;
  url: string;
}

export interface ImageInfo {
  id: string;
  name: string;
  description: string;
  url: string;
}

export interface QuestionInfo {
  id: string;
  question: string;
}

export interface QuizInfo {
  id: string;
  name: string;
  description: string;
  questions: QuestionInfo[];
}

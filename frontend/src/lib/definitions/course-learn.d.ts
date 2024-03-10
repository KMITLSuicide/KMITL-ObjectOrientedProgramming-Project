export interface CompleteQuizResponse{
  "result": boolean,
  "message": string,
  "progress_normalized": number
}

export interface CompleteVideoPostData{
  "id": string,
  "is_complete": boolean
}
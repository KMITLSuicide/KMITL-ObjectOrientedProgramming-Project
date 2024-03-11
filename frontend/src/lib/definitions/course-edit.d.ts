export interface EditQuestionPostData {
  question: string;
  correct: boolean;
}

export interface MaterialEditPostData {
  name: string;
  description: string;
}

export interface MaterialVideoEditPostData extends MaterialEditPostData {
  url: string;
}

export interface MaterialImageEditPostData extends MaterialEditPostData {
  url: string;
}
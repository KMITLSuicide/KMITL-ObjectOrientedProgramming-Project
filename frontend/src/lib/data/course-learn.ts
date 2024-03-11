import api from "~/src/lib/data/api";
import type { CompleteQuizResponse, Progress, ImageInfo, QuizInfo, VideoInfo, SidebarItem } from "~/src/lib/definitions/course-learn";

export async function completeQuiz(courseID: string, quizID: string, data: { "ids": string[] }) {
  try {
    const response = await api.put<CompleteQuizResponse>(`/user/progress/${courseID}/quiz/${quizID}`, data);
    console.log(response);

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

export async function completeVideo(courseID: string, data: Progress) {
  try {
    const response = await api.put<number>(`/user/progress/${courseID}/video`, data);

    if (response.status == 200) {
      return response.data;
    } else {
      return false;
    }
  } catch (error) {
    console.error(error);
    return false;
  }
}

export async function getProgressNormalized(courseID: string) {
  try {
    const response = await api.get<number>(`/user/progress/${courseID}/normalized`);

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

export async function getProgressVideo(courseID: string) {
  try {
    const response = await api.get<Progress[]>(`/user/progress/${courseID}/video`);

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

export async function getProgressVideoNormalized(courseID: string) {
  try {
    const response = await api.get<number>(`/user/progress/${courseID}/video/normalized`);

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

export async function getProgressQuiz(courseID: string) {
  try {
    const response = await api.get<Progress[]>(`/user/progress/${courseID}/quiz`);

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

export async function getProgressQuizNormalized(courseID: string) {
  try {
    const response = await api.get<number>(`/user/progress/${courseID}/quiz/normalized`);

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

export async function getSidebarItemsImage(courseID: string) {
  try {
    const response = await api.get<SidebarItem[]>(`/course/${courseID}/image`);

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

export async function getSidebarItemsVideo(courseID: string) {
  try {
    const response = await api.get<SidebarItem[]>(`/course/${courseID}/video`);

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

export async function getSidebarItemsQuiz(courseID: string) {
  try {
    const response = await api.get<SidebarItem[]>(`/course/${courseID}/quiz`);

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

export async function getVideoInfo(courseID: string, videoID: string) {
  try {
    const response = await api.get<VideoInfo>(`/course/${courseID}/video/${videoID}`);

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

export async function getImageInfo(courseID: string, imageID: string) {
  try {
    const response = await api.get<ImageInfo>(`/course/${courseID}/image/${imageID}`);

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

export async function getQuizInfo(courseID: string, quizID: string) {
  try {
    const response = await api.get<QuizInfo>(`/course/${courseID}/quiz/${quizID}`);

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

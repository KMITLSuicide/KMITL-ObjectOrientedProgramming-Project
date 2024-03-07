import api from "~/src/lib/data/api";
import { type SearchResults } from "~/src/lib/definitions/search";

export async function searchCourse(query: string) {
  try {
    const response = await api.get<SearchResults[]>(`/search/course/${query}`);

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

export async function searchCategory(query: string) {
  try {
    const response = await api.get<SearchResults[]>(`/search/category/${query}`);

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

export async function searchTeacher(query: string) {
  try {
    const response = await api.get<SearchResults[]>(`/search/teacher/${query}`);

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
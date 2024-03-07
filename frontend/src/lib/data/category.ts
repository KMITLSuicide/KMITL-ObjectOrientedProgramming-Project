import api from "~/src/lib/data/api";
import {
  type CategoryInfo,
  type CategoryNames,
} from "~/src/lib/definitions/category";

export async function getCategoryNamesFromAPI() {
  try {
    const response = await api.get<CategoryNames[]>("/category");

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

export async function getCategoryDataWithIDFromAPI(categoryID: string) {
  try {
    const response = await api.get<CategoryInfo>(`/category/${categoryID}`);

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

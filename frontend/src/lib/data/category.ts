import api from "~/src/lib/data/api";

export interface CategoryData {
  _Category__id: string;
  _Category__name: string;
  _Category_courses: any[];
};

export async function getCategoryDataFromAPI() {
  try {
    const response = await api.get<CategoryData>('/category');

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
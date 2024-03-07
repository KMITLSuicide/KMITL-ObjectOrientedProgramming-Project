import { type CourseCardData } from "~/src/lib/definitions/course";

export interface CategoryNames {
  id: string;
  name: string;
}

export interface CategoryInfo {
  id: string;
  name: string;
  courses: CourseCardData[];
}
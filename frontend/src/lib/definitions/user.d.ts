import { Course } from "./course";
export interface User {
  _User__id: string;
  _User__name: string;
  _User__email: string;
  _User__hashed_password: string;
  _User__my_progresses: Progress[];
  _User__latest_progress: null | Progress;
}
interface Teacher extends User {
  _Teacher__my_teachings: Course[]
}
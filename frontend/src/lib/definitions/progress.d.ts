import { Course, CourseMaterialVideo, CourseMaterialQuiz } from "./course"
export interface Progress {
  _Progress__course : Course;
  _Progress__name: string;
  _Progress__progress_videos: ProgressVideo[]
  _Progress__progress_quizes: ProgressQuiz[]
  _Progress__latest_video: ProgressVideo
}
interface ProgressVideo extends CourseMaterialVideo
{
  
}
interface ProgressQuiz extends CourseMaterialQuiz
{

}
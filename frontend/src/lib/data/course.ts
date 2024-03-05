export interface CourseData {
  _Course__id: string;
  _Course__name: string;
  _Course_description: string;
  _Course_price: number;
  _Course_images: any[];
  _Course__quizes: any[];
  _Course__videos: any[];
  _Course__reviews: any[];
  _Course__latest_video: any;
}


export function getFrontendCourseViewData(courseID: string): Frontend.Course {
  const imageNumber = (courseID.charCodeAt(0) % 6) + 1;
  const quizNumber = courseID.charCodeAt(0);
  return {
    id: courseID,
    name: "course name",
    description: "course description",
    category: {
      courses: [],
      id: "category id",
      name: "category name",
    },
    price: 10000,
    images: [
      {
        id: courseID + `image-${imageNumber}`,
        name: "image name",
        description: "image description",
        url: `/course/react/image-${imageNumber}.png`,
      },
    ],
    quizes: [
      {
        id: courseID + `quiz-${quizNumber}`,
        name: "quiz name",
        description: "quiz description",
        questions: [
          {
            question: `quiz-${quizNumber}`,
          },
        ],
      },
    ],
  };
}

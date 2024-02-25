declare namespace Frontend {
  interface CourseQuestion {
    question: string
  }

  interface CourseMaterial {
    id: string,
    name: string,
    description: string
  }

  interface CourseMaterialImage extends CourseMaterial {
    url: string
  }

  interface CourseMaterialQuiz extends CourseMaterial {
    questions: CourseQuestion[]
  }
  
  interface Course {
    id: string
    name: string
    description: string
    price: number
    images: CourseMaterialImage[]
    quizes: CourseMaterialQuiz[]
  }

  interface CourseCatergory {
    id: string
    name: string
    courses: Course[]
  }
}

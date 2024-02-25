export function getFrontendCourseViewData(courseID: string): Frontend.Course {
    const imageNumber = (courseID.charCodeAt(0) % 6) + 1;
    const quizNumber = courseID.charCodeAt(0);
    return({
        id: courseID,
        name: 'course name',
        description: 'course description',
        price: 10000,
        images: [{
            id: courseID + `image-${imageNumber}`,
            name: 'image name',
            description: 'image description',
            url: `/course/react/image-${imageNumber}.png`
        }],
        quizes: [{
            id: courseID + `quiz-${quizNumber}`,
            name: 'quiz name',
            description: 'quiz description',
            questions: [{
                question: `quiz-${quizNumber}`
            }]
        }]
    });
}
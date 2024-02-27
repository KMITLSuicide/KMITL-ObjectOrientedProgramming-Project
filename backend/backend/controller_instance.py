from backend.definitions.controller import Controller
from backend.definitions.user import User
from backend.definitions.progress import Progress, ProgressVideo, ProgressQuiz
from backend.definitions.course import Course,CourseCatergory,CourseMaterialVideo

controller = Controller()

# def test_add_user():
#   controller.add_user(User("Tajdang"))
#   tajdang_user = controller.get_user_by_name("Tajdang")[0]
#   controller.add_category(CourseCatergory("Game Development"))
#   gamedev_category = controller.search_category_by_name("Game Development")
#   if isinstance(gamedev_category, CourseCatergory):
#     gamedev_category.add_course(Course("Unity with Teacher Taj", "this course is for experience unity user", 3000000))
#     unity_course = gamedev_category.get_first_course_by_name("Unity with Teacher Taj")
#     if isinstance(unity_course, Course):
#       #todo add progress to course and set latest video
#       unity_course.add_videos(CourseMaterialVideo("https://www.youtube.com/watch?v=dQw4w9WgXcQ","Rick Astley - Never Gonna Give You Up (Official Music Video)","The official video for “Never Gonna Give You Up” by Rick Astley. "))
#       tajdang_user.add_progress(Progress(unity_course))
#       tajdang_progress = tajdang_user.search_progress_by_name("Unity with Teacher Taj")
#       if isinstance(tajdang_progress, Progress):
#         rick_roll_progress_videos = tajdang_progress.search_video_by_name("Rick Astley - Never Gonna Give You Up (Official Music Video)")
#         if isinstance(rick_roll_progress_videos, ProgressVideo):
#           tajdang_progress.set_latest_video(rick_roll_progress_videos)

# test_add_user()

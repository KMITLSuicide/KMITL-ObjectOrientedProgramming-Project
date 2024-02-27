from backend.definitions.controller import Controller
from backend.definitions.user import User
from backend.definitions.progress import Progress, ProgressVideo
from backend.definitions.course import Course, CourseCatergory, CourseMaterialVideo

controller = Controller()

def test_add_user():
    # Adding a user
    tajdang_user_name = "Tajdang"
    controller.add_user(User(tajdang_user_name))
    tajdang_user = controller.get_users_by_name(tajdang_user_name)[0]

    # Adding a category
    game_dev_category_name = "Game Development"
    controller.add_category(CourseCatergory(game_dev_category_name))
    game_dev_category = controller.search_category_by_name(game_dev_category_name)

    if isinstance(game_dev_category, CourseCatergory):
        # Adding a course
        unity_course_name = "Unity with Teacher Taj"
        unity_course_description = "This course is for experienced Unity users"
        unity_course_price = 3000000

        game_dev_category.add_course(Course(unity_course_name, unity_course_description, unity_course_price))
        unity_course = game_dev_category.get_first_course_by_name(unity_course_name)

        if isinstance(unity_course, Course):
            # Adding course videos
            video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
            video_title = "Rick Astley - Never Gonna Give You Up (Official Music Video)"
            video_description = "The official video for 'Never Gonna Give You Up' by Rick Astley."

            unity_course.add_videos(CourseMaterialVideo(video_url, video_title, video_description))

            # Adding user progress
            user_progress = Progress(unity_course)
            tajdang_user.add_progress(user_progress)
            tajdang_progress = tajdang_user.search_progress_by_name(unity_course_name)

            if isinstance(tajdang_progress, Progress):
                # Setting the latest progress for the user
                tajdang_user.set_latest_progress(tajdang_progress)

                # Setting the latest video for the progress
                rick_roll_progress_videos = tajdang_progress.search_video_by_name(video_title)

                if isinstance(rick_roll_progress_videos, ProgressVideo):
                    tajdang_progress.set_latest_video(rick_roll_progress_videos)

# Calling the test function
test_add_user()

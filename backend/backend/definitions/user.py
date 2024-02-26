from typing import List
import uuid

from backend.definitions.course import Course
from backend.definitions.progress import Progress

class User:
    def __init__(self, name: str) -> None:
        self.__id = uuid.uuid4()
        self.__name = name
        self.__my_learnings: List[Course] = []
        self.__my_progresses: List[Progress] = []
        #Question from Taj to Phak: should I collect latest course in self? if not? what should I do?
        self.__latest_progress = None     
    def get_id(self):
        return self.__id
        
    def get_name(self):
        return self.__name
        
    def get_my_learnings(self):
        return self.__my_learnings
    def add_my_learning(self, course: Course):
        if(isinstance(course, Course)):
            self.__my_learnings.append(course)
            return True
        return False
    def get_latest_video_from_user(self):
        if self.__latest_progress == None:
            return "You haven't studied anything, yet. Study Now!!!"
        latest_course = self.__latest_progress.get_course()
        return latest_course.get_latest_video()
    
    def set_latest_progress(self, progress : Progress):
        self.__latest_progress = progress

    
class Teacher(User):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.__my_teachings: List[Course] = []
        
    def get_my_teachings(self):
        return self.__my_teachings
    
    def add_my_teaching(self, course: Course):
        if(isinstance(course, Course)):
            self.__my_teachings.append(course)
            return True
        return False
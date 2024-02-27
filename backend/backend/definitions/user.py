from typing import List, Union
import uuid

from backend.definitions.course import Course
from backend.definitions.progress import Progress

class User:
    def __init__(self, name: str) -> None:
        self.__id = uuid.uuid4()
        self.__name = name
        self.__my_progresses: List[Progress] = []
        #Question from Taj to Phak: should I collect latest course in self? if not? what should I do?
        self.__latest_progress : Union[Progress, None] = None     
    def get_id(self):
        return self.__id
        
    def get_name(self):
        return self.__name

    def get_latest_video_from_user(self):
        if self.__latest_progress == None:
            return None
        latest_progress_video = self.__latest_progress.get_latest_video()
        return latest_progress_video
    def search_progress_by_name(self, name: str):
        for progress in self.__my_progresses:
            if(progress.get_name() == name):
                return progress
        return None


    def set_latest_progress(self, progress : Progress):
        self.__latest_progress = progress

    def add_progress(self, progress: Progress):
        self.__my_progresses.append(progress)   

    
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
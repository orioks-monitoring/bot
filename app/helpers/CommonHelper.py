import os
import pathlib
from typing import Union

from config import Config


class CommonHelper:

    @staticmethod
    def make_dirs() -> None:
        os.makedirs(os.path.join(Config.BASEDIR, 'users_data', 'cookies'), exist_ok=True)
        os.makedirs(os.path.join(Config.PATH_TO_STUDENTS_TRACKING_DATA, 'marks'), exist_ok=True)
        os.makedirs(os.path.join(Config.PATH_TO_STUDENTS_TRACKING_DATA, 'discipline_sources'), exist_ok=True)
        os.makedirs(os.path.join(Config.PATH_TO_STUDENTS_TRACKING_DATA, 'homeworks'), exist_ok=True)
        os.makedirs(os.path.join(Config.PATH_TO_STUDENTS_TRACKING_DATA, 'news'), exist_ok=True)
        os.makedirs(os.path.join(Config.PATH_TO_STUDENTS_TRACKING_DATA, 'requests', 'questionnaire'), exist_ok=True)
        os.makedirs(os.path.join(Config.PATH_TO_STUDENTS_TRACKING_DATA, 'requests', 'doc'), exist_ok=True)
        os.makedirs(os.path.join(Config.PATH_TO_STUDENTS_TRACKING_DATA, 'requests', 'reference'), exist_ok=True)

    @staticmethod
    def is_correct_convert_to_float(x) -> bool:
        try:
            float(x)
            return True
        except ValueError:
            return False

    @staticmethod
    def safe_delete(path: Union[str, pathlib.Path]) -> None:
        try:
            os.remove(path)
        except FileNotFoundError:
            pass

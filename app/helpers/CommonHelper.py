import os
import pathlib
import traceback
from typing import Union

from config import config


class CommonHelper:
    @staticmethod
    def make_dirs() -> None:
        os.makedirs(
            os.path.join(config.BASEDIR, 'users_data', 'cookies'),
            exist_ok=True,
        )
        os.makedirs(
            os.path.join(config.PATH_TO_STUDENTS_TRACKING_DATA, 'marks'),
            exist_ok=True,
        )
        os.makedirs(
            os.path.join(config.PATH_TO_STUDENTS_TRACKING_DATA, 'homeworks'),
            exist_ok=True,
        )
        os.makedirs(
            os.path.join(config.PATH_TO_STUDENTS_TRACKING_DATA, 'news'),
            exist_ok=True,
        )
        os.makedirs(
            os.path.join(
                config.PATH_TO_STUDENTS_TRACKING_DATA,
                'requests',
                'questionnaire',
            ),
            exist_ok=True,
        )
        os.makedirs(
            os.path.join(
                config.PATH_TO_STUDENTS_TRACKING_DATA, 'requests', 'doc'
            ),
            exist_ok=True,
        )
        os.makedirs(
            os.path.join(
                config.PATH_TO_STUDENTS_TRACKING_DATA, 'requests', 'reference'
            ),
            exist_ok=True,
        )

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

    @staticmethod
    def print_traceback(exception: Exception) -> None:
        traceback.print_exception(
            type(exception), exception, exception.__traceback__
        )

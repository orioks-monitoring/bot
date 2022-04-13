import os
from typing import Union
import pathlib


def safe_delete(path: Union[str, pathlib.Path]) -> None:
    try:
        os.remove(path)
    except FileNotFoundError:
        pass

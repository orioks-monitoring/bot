import os


def safe_delete(path: str) -> None:
    try:
        os.remove(path)
    except FileNotFoundError:
        pass

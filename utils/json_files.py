import json
from typing import Union


class JsonFile:
    @staticmethod
    def save(data: Union[list, dict], filename: str) -> None:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    @staticmethod
    def open(filename: str):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)

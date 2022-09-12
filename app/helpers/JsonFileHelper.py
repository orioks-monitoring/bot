import json
from typing import Union
import aiofiles


class JsonFileHelper:
    @staticmethod
    async def save(data: Union[list, dict], filename: str) -> None:
        async with aiofiles.open(filename, mode='w', encoding='utf-8') as f:
            await f.write(json.dumps(data, indent=2, ensure_ascii=False))

    @staticmethod
    async def open(filename: str):
        async with aiofiles.open(filename, mode='r', encoding='utf-8') as f:
            return json.loads(await f.read())

    @staticmethod
    def convert_dict_keys_to_int(dictionary: dict) -> dict:
        return {int(k): v for k, v in dictionary.items()}

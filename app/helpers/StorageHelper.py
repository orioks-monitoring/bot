from pathlib import Path

import aiofiles


class StorageHelper:
    @staticmethod
    async def save(data: str, filename: Path) -> None:
        async with aiofiles.open(filename, mode='w', encoding='utf-8') as f:
            await f.write(data)

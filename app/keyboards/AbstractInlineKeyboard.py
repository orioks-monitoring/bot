from abc import abstractmethod


class AbstractInlineKeyboard:

    @staticmethod
    @abstractmethod
    async def show(**kwargs) -> None:
        raise NotImplementedError

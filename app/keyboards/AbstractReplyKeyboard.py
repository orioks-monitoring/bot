from abc import abstractmethod


class AbstractReplyKeyboard:
    @staticmethod
    @abstractmethod
    async def show() -> None:
        raise NotImplementedError

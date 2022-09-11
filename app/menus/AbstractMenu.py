from abc import abstractmethod


class AbstractMenu:

    @staticmethod
    @abstractmethod
    async def show(chat_id: int, telegram_user_id: int) -> None:
        raise NotImplementedError

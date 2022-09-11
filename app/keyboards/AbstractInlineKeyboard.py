from abc import abstractmethod


class AbstractInlineKeyboard:

    @staticmethod
    @abstractmethod
    async def show(user_telegram_id: int) -> None:
        raise NotImplementedError

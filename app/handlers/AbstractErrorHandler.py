from abc import abstractmethod

from aiogram import types


class AbstractErrorHandler:

    @staticmethod
    @abstractmethod
    async def process(update: types.Update, exception):
        raise NotImplementedError

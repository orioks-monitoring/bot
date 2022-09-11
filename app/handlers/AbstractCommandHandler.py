from abc import abstractmethod

from aiogram import types


class AbstractCommandHandler:

    @staticmethod
    @abstractmethod
    async def process(message: types.Message, *args, **kwargs):
        raise NotImplementedError()

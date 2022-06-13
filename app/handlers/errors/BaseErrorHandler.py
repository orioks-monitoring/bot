import logging

from aiogram import types
from aiogram.utils.exceptions import MessageNotModified, CantParseEntities, TelegramAPIError

from app.handlers.AbstractErrorHandler import AbstractErrorHandler
from utils.notify_to_user import SendToTelegram


class BaseErrorHandler(AbstractErrorHandler):

    @staticmethod
    async def process(update: types.Update, exception):
        if isinstance(exception, MessageNotModified):
            pass

        if isinstance(exception, CantParseEntities):
            pass

        if isinstance(exception, TelegramAPIError):
            pass

        await SendToTelegram.message_to_admins(message=f'Update: {update} \n{exception}')
        logging.exception(f'Update: {update} \n{exception}')

import logging
from aiogram import types
from aiogram.utils.exceptions import (TelegramAPIError,
                                      MessageNotModified,
                                      CantParseEntities)
from utils.notify_to_user import SendToTelegram


async def errors_handler(update: types.Update, exception):
    if isinstance(exception, MessageNotModified):
        pass

    if isinstance(exception, CantParseEntities):
        pass

    if isinstance(exception, TelegramAPIError):
        pass

    await SendToTelegram.message_to_admins(message=f'Update: {update} \n{exception}')
    logging.exception(f'Update: {update} \n{exception}')

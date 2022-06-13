from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from config import Config


class AdminCommandsMiddleware(BaseMiddleware):
    """
        Middleware, разрешающее использовать команды Админов только пользователям из `config.TELEGRAM_ADMIN_IDS_LIST`
    """

    # pylint: disable=unused-argument
    async def on_process_message(self, message: types.Message, *args, **kwargs):
        if message.get_command() in ('/stat',) and message.from_user.id not in Config.TELEGRAM_ADMIN_IDS_LIST:
            raise CancelHandler()

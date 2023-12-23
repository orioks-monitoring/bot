import logging

from aiogram import types

from app.handlers.AbstractErrorHandler import AbstractErrorHandler
from app.helpers import MessageToAdminsHelper


class BaseErrorHandler(AbstractErrorHandler):
    @staticmethod
    async def process(update: types.Update, exception: Exception):
        await MessageToAdminsHelper.send(
            message=f'Update: {update} \n{exception}'
        )
        logging.exception('Update: %s \n%s', update, exception)

from aiogram import types
from aiogram.utils import markdown

import app
from app.forms import OrioksAuthForm
from app.handlers import AbstractCommandHandler

import db.user_status
import db.user_first_add


class OrioksAuthStartCommandHandler(AbstractCommandHandler):

    @staticmethod
    async def process(message: types.Message, *args, **kwargs):
        if db.user_status.get_user_orioks_authenticated_status(user_telegram_id=message.from_user.id):
            return await message.reply(
                markdown.text(
                    markdown.hbold('Ты уже выполнил вход в аккаунт ОРИОКС.'),
                    markdown.text(),
                    markdown.text('Выполнить выход из аккаунта ОРИОКС: /logout'),
                    sep='\n',
                )
            )
        await OrioksAuthForm.login.set()
        await app.bot.send_message(
            message.chat.id,
            markdown.text(
                markdown.text('Я беспокоюсь, мои данные могут быть перехвачены?'),
                markdown.text(),
                markdown.text('Отменить авторизацию и получить дополнительную информацию:', markdown.hbold('/cancel')),
            ),
        )
        await message.reply(
            markdown.text(
                markdown.hbold('🔒 Введи логин ОРИОКС'),
            ),
            reply_markup=types.ReplyKeyboardRemove()
        )

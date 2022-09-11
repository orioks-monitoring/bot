from aiogram import types

from app.keyboards import AbstractReplyKeyboard


class AuthorizationReplyKeyboard(AbstractReplyKeyboard):

    @staticmethod
    async def show() -> types.ReplyKeyboardMarkup:
        keyboard_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        keyboard_markup.row(types.KeyboardButton('Авторизация'))

        more_btns_text = ('Руководство', 'О проекте')
        keyboard_markup.add(*(types.KeyboardButton(text) for text in more_btns_text))
        return keyboard_markup

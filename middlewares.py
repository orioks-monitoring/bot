import aiogram.utils.markdown as md
from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

import db

inline_btn_user_agreement_accept = types.InlineKeyboardButton(
    'Принять пользовательское соглашение',
    callback_data='button_user_agreement_accept'
)
inline_agreement_accept = types.InlineKeyboardMarkup().add(inline_btn_user_agreement_accept)


class UserAgreementMiddleware(BaseMiddleware):
    async def on_process_message(self, message: types.Message, *args, **kwargs):
        db.user_first_add_to_db(user_telegram_id=message.from_user.id)
        if not db.get_user_agreement_status(user_telegram_id=message.from_user.id):
            await message.reply(
                md.text(
                    md.text('Для получения доступа к боту, необходимо принять пользовательское соглашение:'),
                    md.text('<url>'),
                    sep='\n',
                ),
                parse_mode=types.ParseMode.MARKDOWN, reply_markup=inline_agreement_accept
            )
            raise CancelHandler()


class UserOrioksAttemptsMiddleware(BaseMiddleware):
    async def on_process_message(self, message: types.Message, *args, **kwargs):
        print(db.get_user_orioks_attempts(user_telegram_id=message.from_user.id))
        if db.get_user_orioks_attempts(user_telegram_id=message.from_user.id) > 10:  # todo: to config
            await message.reply(
                md.text(
                    md.bold('Вы совершили подозрительно много попыток авторизации ОРИОКС аккаунта'),
                    md.text('Возможно, Вы нарушаете [правила](<user agreement url>), с которыми согласились'),
                    md.text(),
                    md.text('Связь с поддержкой Бота: <support url>'),
                    sep='\n',
                ),
                parse_mode=types.ParseMode.MARKDOWN, reply_markup=types.ReplyKeyboardRemove(),
            )
            raise CancelHandler()

import aiogram.utils.markdown as md
from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

import config
import db.user_first_add
import db.user_status

inline_btn_user_agreement_accept = types.InlineKeyboardButton(
    'Принять пользовательское соглашение',
    callback_data='button_user_agreement_accept'
)
inline_agreement_accept = types.InlineKeyboardMarkup().add(inline_btn_user_agreement_accept)


class UserAgreementMiddleware(BaseMiddleware):
    """Middleware, блокирующее дальнейшее использование Бота, если не принято пользовательское соглашение"""

    async def on_process_message(self, message: types.Message, *args, **kwargs):
        db.user_first_add.user_first_add_to_db(user_telegram_id=message.from_user.id)
        if not db.user_status.get_user_agreement_status(user_telegram_id=message.from_user.id):
            await message.reply(
                md.text(
                    md.text('Для получения доступа к Боту, необходимо принять Пользовательское соглашение:'),
                    md.text('https://orioks-monitoring.github.io/bot/rules'),
                    sep='\n',
                ),
                reply_markup=inline_agreement_accept,
                disable_web_page_preview=True,
            )
            raise CancelHandler()


class UserOrioksAttemptsMiddleware(BaseMiddleware):
    """Middleware, блокирующее дальнейшее использование Бота, если превышено максимальное количество попыток входа в
    аккаунт ОРИОКС"""

    async def on_process_message(self, message: types.Message, *args, **kwargs):
        if db.user_status.get_user_orioks_attempts(
                user_telegram_id=message.from_user.id) > config.ORIOKS_MAX_LOGIN_TRIES:
            await message.reply(
                md.text(
                    md.hbold('Ты совершил подозрительно много попыток входа в аккаунт ОРИОКС.'),
                    md.text('Возможно, ты нарушаешь <a href="https://orioks-monitoring.github.io/bot/rules">Пользовательское соглашение</a>, с которым согласился.'),
                    md.text(),
                    md.text('Связаться с поддержкой Бота: @orioks_monitoring_support'),
                    sep='\n',
                ),
                reply_markup=types.ReplyKeyboardRemove(),
                disable_web_page_preview=True,
            )
            raise CancelHandler()


class AdminCommandsMiddleware(BaseMiddleware):
    """Middleware, разрешающее использовать команды Админов только пользователям из `config.TELEGRAM_ADMIN_IDS_LIST`"""

    async def on_process_message(self, message: types.Message, *args, **kwargs):
        if message.get_command() in ('/stat',) and message.from_user.id not in config.TELEGRAM_ADMIN_IDS_LIST:
            raise CancelHandler()

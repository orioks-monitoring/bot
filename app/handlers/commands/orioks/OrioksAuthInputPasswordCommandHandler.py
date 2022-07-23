import asyncio

from aiogram import types
from aiogram.utils import markdown

import app
from app.exceptions import OrioksInvalidLoginCredentialsException
from app.forms import OrioksAuthForm
from app.handlers import AbstractCommandHandler
from app.helpers import OrioksHelper, TelegramMessageHelper, UserHelper, AdminHelper
from app.menus.orioks import OrioksAuthFailedMenu
from app.menus.start import StartMenu
from config import config


class OrioksAuthInputPasswordCommandHandler(AbstractCommandHandler):

    @staticmethod
    async def process(message: types.Message, *args, **kwargs):
        state = kwargs.get('state', None)
        UserHelper.increment_login_attempt_count(user_telegram_id=message.from_user.id)
        if UserHelper.get_login_attempt_count(user_telegram_id=message.from_user.id) > config.ORIOKS_MAX_LOGIN_TRIES:
            return await message.reply(
                markdown.text(
                    markdown.hbold('Ошибка! Ты истратил все попытки входа в аккаунт ОРИОКС.'),
                    markdown.text(),
                    markdown.text('Связаться с поддержкой Бота: @orioks_monitoring_support'),
                    sep='\n',
                )
            )
        await OrioksAuthForm.next()
        await state.update_data(password=message.text)
        if UserHelper.is_user_orioks_authenticated(user_telegram_id=message.from_user.id):
            await state.finish()
            await app.bot.delete_message(message.chat.id, message.message_id)
            return await app.bot.send_message(
                chat_id=message.chat.id,
                text=markdown.text('Авторизация уже выполнена')
            )
        async with state.proxy() as data:
            sticker_message = await app.bot.send_sticker(
                message.chat.id,
                config.TELEGRAM_STICKER_LOADER,
            )
            try:
                await OrioksHelper.orioks_login_save_cookies(user_login=data['login'],
                                                             user_password=data['password'],
                                                             user_telegram_id=message.from_user.id)
                UserHelper.update_authorization_status(
                    user_telegram_id=message.from_user.id,
                    is_authenticated=True
                )
                await StartMenu.show(chat_id=message.chat.id, telegram_user_id=message.from_user.id)
                await app.bot.send_message(
                    message.chat.id,
                    markdown.text(
                        markdown.text('Вход в аккаунт ОРИОКС выполнен!')
                    )
                )
                AdminHelper.increase_success_logins()
            except OrioksInvalidLoginCredentialsException:
                AdminHelper.increase_failed_logins()
                await OrioksAuthFailedMenu.show(chat_id=message.chat.id, telegram_user_id=message.from_user.id)
            except (asyncio.TimeoutError, TypeError):
                await app.bot.send_message(
                    chat_id=message.chat.id,
                    text=markdown.text(
                        markdown.hbold('🔧 Сервер ОРИОКС в данный момент недоступен!'),
                        markdown.text('Пожалуйста, попробуй ещё раз через 15 минут.'),
                        sep='\n',
                    )
                )
                await TelegramMessageHelper.message_to_admins(message='Сервер ОРИОКС не отвечает')
                await OrioksAuthFailedMenu.show(chat_id=message.chat.id, telegram_user_id=message.from_user.id)
        await app.bot.delete_message(message.chat.id, message.message_id)
        await state.finish()

        await app.bot.delete_message(sticker_message.chat.id, sticker_message.message_id)

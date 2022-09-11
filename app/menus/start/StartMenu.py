from aiogram.utils import markdown

import app
from app.helpers import UserHelper
from app.menus.AbstractMenu import AbstractMenu

from app.keyboards.notify_settings import NotifySettingsReplyKeyboard


class StartMenu(AbstractMenu):

    @staticmethod
    async def show(chat_id: int, telegram_user_id: int) -> None:
        UserHelper.create_user_if_not_exist(user_telegram_id=telegram_user_id)
        if not UserHelper.is_user_orioks_authenticated(user_telegram_id=telegram_user_id):
            await app.bot.send_message(
                chat_id,
                markdown.text(
                    markdown.text('Привет!'),
                    markdown.text('Этот Бот поможет тебе узнавать об изменениях в твоём ОРИОКС в режиме реального времени.'),
                    markdown.text(),
                    markdown.text('Ознакомиться с Информацией о проекте: /faq'),
                    markdown.text('Ознакомиться с Инструкцией: /manual'),
                    markdown.text('Выполнить вход в аккаунт ОРИОКС: /login'),
                    sep='\n',
                ),
                reply_markup=await NotifySettingsReplyKeyboard.show(),
            )
        else:
            await app.bot.send_message(
                chat_id,
                markdown.text(
                    markdown.text('Настроить уведомления: /notifysettings'),
                    markdown.text(),
                    markdown.text('Ознакомиться с Инструкцией: /manual'),
                    markdown.text('Выполнить выход из аккаунта ОРИОКС: /logout'),
                    sep='\n',
                ),
                reply_markup=await NotifySettingsReplyKeyboard.show(),
            )

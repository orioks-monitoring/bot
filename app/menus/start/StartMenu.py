from aiogram.utils import markdown

import app
from app.menus.AbstractMenu import AbstractMenu

import db.user_status
import keyboards
import db.user_first_add


class StartMenu(AbstractMenu):

    @staticmethod
    async def show(chat_id: int, telegram_user_id: int) -> None:
        db.user_first_add.user_first_add_to_db(user_telegram_id=telegram_user_id)
        if not db.user_status.get_user_orioks_authenticated_status(user_telegram_id=telegram_user_id):
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
                reply_markup=keyboards.main_menu_keyboard(first_btn_text='Авторизация'),
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
                reply_markup=keyboards.main_menu_keyboard(first_btn_text='Настройка уведомлений')
            )

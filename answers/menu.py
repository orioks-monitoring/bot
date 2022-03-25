import aiogram.utils.markdown as md

import db
import keyboards
from main import bot


async def menu_command(chat_id: int, user_id: int):
    db.user_first_add_to_db(user_telegram_id=user_id)
    if not db.get_user_orioks_authenticated_status(user_telegram_id=user_id):
        await bot.send_message(
            chat_id,
            md.text(
                md.text('Привет!'),
                md.text('Этот Бот поможет тебе узнавать об изменениях в твоём ОРИОКС в режиме реального времени.'),
                md.text(),
                md.text('Ознакомиться с Информацией о проекте: /faq'),
                md.text('Ознакомиться с Инструкцией: /manual'),
                md.text('Выполнить вход в аккаунт ОРИОКС: /login'),
                sep='\n',
            ),
            reply_markup=keyboards.main_menu_keyboard(first_btn_text='Авторизация')
        )
    else:
        await bot.send_message(
            chat_id,
            md.text(
                md.text('Настроить уведомления: /notifysettings'),
                md.text(),
                md.text('Ознакомиться с Инструкцией: /manual'),
                md.text('Выполнить выход из аккаунта ОРИОКС: /logout'),
                sep='\n',
            ),
            reply_markup=keyboards.main_menu_keyboard(first_btn_text='Настройка уведомлений')
        )


async def menu_if_failed_login(chat_id: int, user_id: int):
    if not db.get_user_orioks_authenticated_status(user_telegram_id=user_id):
        await bot.send_message(
            chat_id,
            md.text(
                md.hbold('Ошибка авторизации!'),
                md.text('Попробуйте ещё раз: /login'),
                sep='\n',
            ),
            reply_markup=keyboards.main_menu_keyboard(first_btn_text='Авторизация')
        )

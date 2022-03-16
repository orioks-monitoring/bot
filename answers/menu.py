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
                md.text('Этот бот поможет тебе сразу узнавать о новых оценках в ориоксе.'),
                md.text(),
                md.text('Ознакомься с инструкцией: /manual'),
                md.text('Или выполни вход: /login'),
                sep='\n',
            ),
            reply_markup=keyboards.main_menu_keyboard(first_btn_text='Авторизация')
        )
    else:
        await bot.send_message(
            chat_id,
            md.text(
                md.text('Привет!'),
                md.text('Настроить уведомления: /notifysettings'),
                md.text(),
                md.text('Ознакомиться с Инструкций: /manual'),
                md.text('Выполнить выход из аккаунта ориокс: /logout'),
                sep='\n',
            ),
            reply_markup=keyboards.main_menu_keyboard(first_btn_text='Настройка уведомлений')
        )

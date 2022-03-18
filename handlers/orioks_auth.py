import logging
import os

import aiogram.utils.markdown as md
from aiogram import types
from aiogram.dispatcher import FSMContext

import config
import db
import keyboards
import utils.exeptions
import utils.orioks
from answers import menu
from forms import Form
from main import bot

logger = logging.getLogger(__name__)


async def cmd_start(message: types.Message):
    """
    @dp.message_handler(text='Авторизация')
    @dp.message_handler(commands='login')
    """
    if db.get_user_orioks_authenticated_status(user_telegram_id=message.from_user.id):
        return await message.reply(
            md.text(
                md.bold('Вы уже выполнили авторизацию аккаунта ОРИОКС'),
                md.text(),
                md.text('Выход из аккаунта ОРИОКС: /logout'),
                sep='\n',
            )
        )
    await Form.login.set()
    await bot.send_message(
        message.chat.id,
        md.text(
            md.text('Я беспокоюсь, что мои данные будут перехвачены.'),
            md.text('Отмена авторизации и получение дополнительной информации:', md.bold('/cancel')),
        ),
    )
    await message.reply(
        md.text(
            md.bold('🔒 Введите логин ориокс'),
        ),
        reply_markup=types.ReplyKeyboardRemove()
    )


async def cancel_handler(message: types.Message, state: FSMContext):
    """
    @dp.message_handler(state='*', commands='cancel')
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    await state.finish()
    await message.reply(
        md.text(
            md.bold('Авторизация отменена'),
            md.text('Если боишься вводить свои данные, ознакомься с <faq #why is it secure url>'),
            sep='\n',
        ),
        reply_markup=keyboards.main_menu_keyboard(first_btn_text='Авторизация'),
    )


async def process_login_invalid(message: types.Message):
    """
    @dp.message_handler(lambda message: not message.text.isdigit(), state=Form.login)
    """
    return await message.reply(
        md.text(
            md.text('Логин должен состоять только из цифр'),
            md.text('Введите логин (только цифры)'),
            sep='\n'
        ),
    )


async def process_login(message: types.Message, state: FSMContext):
    """
    @dp.message_handler(state=Form.login)
    """
    async with state.proxy() as data:
        data['login'] = int(message.text)

    await Form.next()
    await message.reply(
        md.text(
            md.bold('Введите пароль ориокс'),
            md.text(),
            md.text(
                md.italic('🔒 Пароль используется только для однократной авторизации'),
                md.italic('Он не хранится на сервере'),
                md.italic('Узнать подробнее: <faq #why is it secure url>'),
                sep='. '
            ),
            sep='\n',
        ),
    )


async def process_password(message: types.Message, state: FSMContext):
    """
    @dp.message_handler(state=Form.password)
    """
    db.update_inc_user_orioks_attempts(user_telegram_id=message.from_user.id)
    if db.get_user_orioks_attempts(user_telegram_id=message.from_user.id) > 10:  # todo: to config
        return await message.reply(
            md.text(
                md.bold('Ошибка!'),
                md.text('Связь с поддержкой Бота: <support url>'),
                sep='\n',
            )
        )
    await Form.next()
    await state.update_data(password=message.text)
    async with state.proxy() as data:
        await bot.send_message(
            message.chat.id,
            md.text(
                md.text('Логин:', md.bold(data['login'])),
                md.text('Пароль:', md.code(data['password'])),
                sep='\n',
            ),
        )
    await bot.delete_message(message.chat.id, message.message_id)
    await state.finish()
    sticker_message = await bot.send_sticker(
        message.chat.id,
        "CAACAgIAAxkBAAEEIlpiLSwO28zurkSJGRj6J9SLBIAHYQACIwADKA9qFCdRJeeMIKQGIwQ",  # todo: to config
    )
    try:
        await utils.orioks.orioks_login_save_cookies(user_login=data['login'],
                                                     user_password=data['password'],
                                                     user_telegram_id=message.from_user.id)
        db.update_user_orioks_authenticated_status(
            user_telegram_id=message.from_user.id,
            is_user_orioks_authenticated=True
        )
        await bot.send_message(
            message.chat.id,
            md.text(
                md.text('Вход выполнен!')
            )
        )
    except utils.exeptions.OrioksInvalidLoginCredsError:
        await bot.send_message(
            message.chat.id,
            md.text(
                md.text('Ошибка входа в аккаунт ОРИОКС!')
            )
        )
    await bot.delete_message(sticker_message.chat.id, sticker_message.message_id)
    await menu.menu_command(chat_id=message.chat.id, user_id=message.from_user.id)


async def orioks_logout(message: types.Message):
    # todo: delete cookies
    await message.reply(
        md.text(
            md.bold('Выход из аккаунта ОРИОКС выполнен'),
            md.text('Теперь Вы НЕ будете получать уведомления от Бота'),
            sep='\n',
        ),
        reply_markup=keyboards.main_menu_keyboard(first_btn_text='Авторизация'),
    )
    db.update_user_orioks_authenticated_status(
        user_telegram_id=message.from_user.id,
        is_user_orioks_authenticated=False
    )
    try:
        os.remove(os.path.join(config.BASEDIR, 'users_data', 'cookies', f'{message.from_user.id}.pkl'))
    except FileNotFoundError:
        pass  # todo: to logger

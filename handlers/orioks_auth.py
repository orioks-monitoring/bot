import asyncio

import aiogram.utils.markdown as md
from aiogram import types
from aiogram.dispatcher import FSMContext

import config
import db.user_status
import db.admins_statistics
import keyboards
import utils.exeptions
import utils.orioks
from answers import menu
from forms import Form
from main import bot
from utils import notify_to_user


async def cmd_start(message: types.Message):
    """
    @dp.message_handler(text='Авторизация')
    @dp.message_handler(commands='login')
    """
    if db.user_status.get_user_orioks_authenticated_status(user_telegram_id=message.from_user.id):
        return await message.reply(
            md.text(
                md.hbold('Ты уже выполнил вход в аккаунт ОРИОКС.'),
                md.text(),
                md.text('Выполнить выход из аккаунта ОРИОКС: /logout'),
                sep='\n',
            )
        )
    await Form.login.set()
    await bot.send_message(
        message.chat.id,
        md.text(
            md.text('Я беспокоюсь, мои данные могут быть перехвачены?'),
            md.text(),
            md.text('Отменить авторизацию и получить дополнительную информацию:', md.hbold('/cancel')),
        ),
    )
    await message.reply(
        md.text(
            md.hbold('🔒 Введи логин ОРИОКС'),
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

    await state.finish()
    await message.reply(
        md.text(
            md.hbold('Авторизация отменена.'),
            md.text('Если ты боишься вводить свои данные, ознакомься со следующей <a href="https://orioks-monitoring.github.io/bot/faq#почему-это-безопасно">информацией</a>'),
            sep='\n',
        ),
        reply_markup=keyboards.main_menu_keyboard(first_btn_text='Авторизация'),
        disable_web_page_preview=True,
    )


async def process_login_invalid(message: types.Message):
    """
    @dp.message_handler(lambda message: not message.text.isdigit(), state=Form.login)
    """
    return await message.reply(
        md.text(
            md.text('Логин должен состоять только из цифр.'),
            md.text('Введи логин (только цифры):'),
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
            md.hbold('Введи пароль ОРИОКС:'),
            md.text(),
            md.text(
                md.hitalic('🔒 Пароль используется только для однократной авторизации'),
                md.hitalic('Он не хранится на сервере и будет удалён из истории сообщений'),
                md.text('Узнать подробнее можно <a href="https://orioks-monitoring.github.io/bot/faq#почему-это-безопасно">здесь</a>'),
                sep='. '
            ),
            sep='\n',
        ),
        disable_web_page_preview=True,
    )


async def process_password(message: types.Message, state: FSMContext):
    """
    @dp.message_handler(state=Form.password)
    """
    db.user_status.update_inc_user_orioks_attempts(user_telegram_id=message.from_user.id)
    if db.user_status.get_user_orioks_attempts(user_telegram_id=message.from_user.id) > config.ORIOKS_MAX_LOGIN_TRIES:
        return await message.reply(
            md.text(
                md.hbold('Ошибка! Ты истратил все попытки входа в аккаунт ОРИОКС.'),
                md.text(),
                md.text('Связаться с поддержкой Бота: @orioks_monitoring_support'),
                sep='\n',
            )
        )
    await Form.next()
    await state.update_data(password=message.text)
    async with state.proxy() as data:
        sticker_message = await bot.send_sticker(
            message.chat.id,
            config.TELEGRAM_STICKER_LOADER,
        )
        try:
            await utils.orioks.orioks_login_save_cookies(user_login=data['login'],
                                                         user_password=data['password'],
                                                         user_telegram_id=message.from_user.id)
            db.user_status.update_user_orioks_authenticated_status(
                user_telegram_id=message.from_user.id,
                is_user_orioks_authenticated=True
            )
            await menu.menu_command(chat_id=message.chat.id, user_id=message.from_user.id)
            await bot.send_message(
                message.chat.id,
                md.text(
                    md.text('Вход в аккаунт ОРИОКС выполнен!')
                )
            )
            db.admins_statistics.update_inc_admins_statistics_row_name(
                row_name=db.admins_statistics.AdminsStatisticsRowNames.orioks_success_logins
            )
        except utils.exeptions.OrioksInvalidLoginCredsError:
            db.admins_statistics.update_inc_admins_statistics_row_name(
                row_name=db.admins_statistics.AdminsStatisticsRowNames.orioks_failed_logins
            )
            await menu.menu_if_failed_login(chat_id=message.chat.id, user_id=message.from_user.id)
        except (asyncio.TimeoutError, TypeError) as e:
            await message.reply(md.text(
                md.hbold('🔧 Сервер ОРИОКС в данный момент недоступен!'),
                md.text('Пожалуйста, попробуй ещё раз через 15 минут.'),
                sep='\n',
            ))
            await notify_to_user.notify_admins(message='Сервер ОРИОКС не отвечает')
            await menu.menu_if_failed_login(chat_id=message.chat.id, user_id=message.from_user.id)
    await bot.delete_message(message.chat.id, message.message_id)
    await state.finish()

    await bot.delete_message(sticker_message.chat.id, sticker_message.message_id)


async def orioks_logout(message: types.Message):
    await message.reply(
        md.text(
            md.hbold('Выход из аккаунта ОРИОКС выполнен.'),
            md.text('Теперь ты НЕ будешь получать уведомления от Бота.'),
            sep='\n',
        ),
        reply_markup=keyboards.main_menu_keyboard(first_btn_text='Авторизация'),
    )
    db.user_status.update_user_orioks_authenticated_status(
        user_telegram_id=message.from_user.id,
        is_user_orioks_authenticated=False
    )
    utils.orioks.make_orioks_logout(user_telegram_id=message.from_user.id)

from main import bot
from aiogram import types
import answers
import db


async def callback_query_handler_user_agreement(callback_query: types.CallbackQuery):
    """@dp.callback_query_handler(lambda c: c.data == 'button_user_agreement_accept')"""
    if db.user_status.get_user_agreement_status(user_telegram_id=callback_query.from_user.id):
        return await bot.answer_callback_query(
            callback_query.id,
            text='Пользовательское соглашение уже принято.', show_alert=True)
    db.user_status.update_user_agreement_status(
        user_telegram_id=callback_query.from_user.id,
        is_user_agreement_accepted=True
    )
    await bot.answer_callback_query(callback_query.id)
    answer_message = await bot.send_message(callback_query.from_user.id, 'Пользовательское соглашение принято!')
    await answers.menu.menu_command(chat_id=answer_message.chat.id, user_id=callback_query.from_user.id)


async def callback_query_handler_notify_settings_btns(callback_query: types.CallbackQuery):
    """@dp.callback_query_handler(lambda c: c.data in config.notify_settings_btns)"""
    _row_name = callback_query.data.split('-')[1]
    if callback_query.data in ['notify_settings-discipline_sources']:
        return await bot.answer_callback_query(
            callback_query.id,
            text='Эта категория ещё недоступна.', show_alert=True
        )
    db.notify_settings.update_user_notify_settings(
        user_telegram_id=callback_query.from_user.id,
        row_name=_row_name,
        to_value=not db.notify_settings.get_user_notify_settings_to_dict(
            user_telegram_id=callback_query.from_user.id)[_row_name],
    )
    await answers.settings.send_user_settings(user_id=callback_query.from_user.id, callback_query=callback_query)

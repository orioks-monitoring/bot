from aiogram import types

from app.keyboards import AbstractInlineKeyboard


class UserAgreementInlineKeyboard(AbstractInlineKeyboard):

    @staticmethod
    async def show(**kwargs) -> types.InlineKeyboardMarkup:
        inline_btn_user_agreement_accept = types.InlineKeyboardButton(
            'Принять пользовательское соглашение',
            callback_data='button_user_agreement_accept'
        )
        inline_agreement_accept = types.InlineKeyboardMarkup().add(inline_btn_user_agreement_accept)
        return inline_agreement_accept

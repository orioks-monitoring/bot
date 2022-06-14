from typing import Type

from aiogram import Dispatcher

from config import config

from .AbstractCommandHandler import AbstractCommandHandler
from .AbstractCallbackHandler import AbstractCallbackHandler

__all__ = ['AbstractCommandHandler', 'AbstractCallbackHandler']

from .errors import BaseErrorHandler
from ..forms import OrioksAuthForm


def register_handlers(dispatcher: Dispatcher) -> None:
    from .commands.general import StartCommandHandler, ManualCommandHandler, FAQCommandHandler
    from .commands.orioks import OrioksAuthStartCommandHandler, OrioksLogoutCommandHandler, \
        OrioksAuthCancelCommandHandler, OrioksAuthInputLoginCommandHandler, OrioksAuthInputPasswordCommandHandler
    from .commands.settings import NotificationSettingsCommandHandler
    from .commands.admins import AdminStatisticsCommandHandler
    from .callbacks import UserAgreementCallbackHandler, SettingsCallbackHandler

    # General commands
    _register_message_handler(dispatcher, StartCommandHandler, text=['Меню'], commands=['start'])
    _register_message_handler(dispatcher, ManualCommandHandler, text=['Руководство'], commands=['manual'])
    _register_message_handler(dispatcher, FAQCommandHandler, text=['О проекте'], commands=['faq'])

    # Orioks commands
    _register_message_handler(dispatcher, OrioksAuthStartCommandHandler, text=['Авторизация'], commands=['login'])
    _register_message_handler(dispatcher, OrioksAuthCancelCommandHandler, commands=['cancel'], state='*')
    _register_message_handler(dispatcher, OrioksAuthInputLoginCommandHandler, state=OrioksAuthForm.login)
    _register_message_handler(dispatcher, OrioksAuthInputPasswordCommandHandler, state=OrioksAuthForm.password)
    _register_message_handler(dispatcher, OrioksLogoutCommandHandler, commands=['logout'])

    # Settings commands
    _register_message_handler(dispatcher, NotificationSettingsCommandHandler, text=['Настройка уведомлений'], commands=['notifysettings'])

    # Admin commands
    _register_message_handler(dispatcher, AdminStatisticsCommandHandler, commands=['stat'])

    # Callbacks
    dispatcher.register_callback_query_handler(
        UserAgreementCallbackHandler.process, lambda c: c.data == 'button_user_agreement_accept'
    )
    dispatcher.register_callback_query_handler(
        SettingsCallbackHandler.process, lambda c: c.data in config.notify_settings_btns
    )

    # Errors
    dispatcher.register_errors_handler(BaseErrorHandler.process, exception=Exception)


def _register_message_handler(
        dispatcher_: Dispatcher, handler_class: Type[AbstractCommandHandler],
        text: list = None, commands: list = None, state=None
):
    if text is not None:
        dispatcher_.register_message_handler(handler_class.process, text=text, state=state)

    if commands is not None:
        dispatcher_.register_message_handler(handler_class.process, commands=commands, state=state)

    if text is None and commands is None and state is not None:
        dispatcher_.register_message_handler(handler_class.process, state=state)

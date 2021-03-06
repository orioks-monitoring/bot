import config
from forms import Form
from handlers import commands, orioks_auth, notify_settings, admins, callback_queries, errors


def handles_register(dp):
    """commands"""
    dp.register_message_handler(commands.start_cmd_handler, text=['Меню'])
    dp.register_message_handler(commands.start_cmd_handler, commands=['start'])

    dp.register_message_handler(commands.msg_manual, text=['Руководство'])
    dp.register_message_handler(commands.msg_manual, commands=['manual'])

    dp.register_message_handler(commands.msg_faq, text=['О проекте'])
    dp.register_message_handler(commands.msg_faq, commands=['faq'])

    """orioks_auth"""
    dp.register_message_handler(orioks_auth.cmd_start, text=['Авторизация'])
    dp.register_message_handler(orioks_auth.cmd_start, commands=['login'])


    dp.register_message_handler(orioks_auth.orioks_logout, commands=['logout'])

    dp.register_message_handler(orioks_auth.cancel_handler, commands=['cancel'], state='*')

    dp.register_message_handler(orioks_auth.process_login_invalid, lambda message: not message.text.isdigit(),
                                state=Form.login)

    dp.register_message_handler(orioks_auth.process_login, state=Form.login)

    dp.register_message_handler(orioks_auth.process_password, state=Form.password)

    """notify settings"""
    dp.register_message_handler(notify_settings.user_settings, text=['Настройка уведомлений'])
    dp.register_message_handler(notify_settings.user_settings, commands=['notifysettings'])

    """admins"""
    dp.register_message_handler(admins.admin_get_statistics, commands=['stat'])

    """callback queries"""
    dp.register_callback_query_handler(
        callback_queries.callback_query_handler_user_agreement,
        lambda c: c.data == 'button_user_agreement_accept'
    )
    dp.register_callback_query_handler(
        callback_queries.callback_query_handler_notify_settings_btns,
        lambda c: c.data in config.notify_settings_btns
    )

    """errors"""
    dp.register_errors_handler(errors.errors_handler, exception=Exception)

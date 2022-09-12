from typing import Dict

from app.models import session
from app.models.admins import AdminStatistics
from app.models.users import UserStatus, UserNotifySettings


class AdminHelper:
    @staticmethod
    def get_statistics_object() -> AdminStatistics:
        return AdminStatistics.find_one(id=1)

    @staticmethod
    def increase_success_logins():
        statistics = AdminHelper.get_statistics_object()
        statistics.success_logins += 1
        statistics.save()

    @staticmethod
    def increase_failed_logins():
        statistics = AdminHelper.get_statistics_object()
        statistics.failed_logins += 1
        statistics.save()

    @staticmethod
    def increase_scheduled_requests():
        statistics = AdminHelper.get_statistics_object()
        statistics.scheduled_requests += 1
        statistics.save()

    @staticmethod
    def get_user_status_statistics(**kwargs):
        users_with_accepted_agreement = UserStatus.query.filter_by(**kwargs)
        return users_with_accepted_agreement.count()

    @staticmethod
    def get_count_users_statistics() -> Dict:
        users_agreement_accepted = AdminHelper.get_user_status_statistics(
            agreement_accepted=True
        )
        users_agreement_discarded = AdminHelper.get_user_status_statistics(
            agreement_accepted=False
        )

        users_orioks_authentication = AdminHelper.get_user_status_statistics(
            authenticated=True
        )
        users_orioks_no_authentication = (
            AdminHelper.get_user_status_statistics(authenticated=False)
        )

        all_users = users_agreement_discarded + users_agreement_accepted
        all_orioks_users = (
            users_orioks_no_authentication + users_orioks_authentication
        )
        return {
            'Приняли пользовательское соглашение': f'{users_agreement_accepted} / {all_users}',
            'Выполнили вход в ОРИОКС': f'{users_orioks_authentication} / {all_orioks_users}',
        }

    @staticmethod
    def get_count_notify_settings_by_row_name(row_name: str) -> int:
        if row_name not in (
            'marks',
            'news',
            'discipline_sources',
            'homeworks',
            'requests',
        ):
            raise Exception(
                'select_count_notify_settings_row_name() -> row_name must only be in ('
                'marks, news, discipline_sources, homeworks, requests)'
            )

        users_count = (
            session.query(UserStatus)
            .join(
                UserNotifySettings,
                UserStatus.user_telegram_id
                == UserNotifySettings.user_telegram_id,
            )
            .filter(
                UserStatus.authenticated == True,
                getattr(UserNotifySettings, row_name) == True,
            )
            .count()
        )

        return int(users_count)

    @staticmethod
    def get_general_statistics():
        statistics_object = AdminHelper.get_statistics_object()
        successful_login_percent = f'{statistics_object.success_logins} / {statistics_object.success_logins + statistics_object.failed_logins}'
        return {
            'Запланированные успешные запросы на сервера ОРИОКС': statistics_object.scheduled_requests,
            'Успешные попытки авторизации ОРИОКС': successful_login_percent,
        }

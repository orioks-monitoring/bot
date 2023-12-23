from app.exceptions import DatabaseException
from app.models.users import UserStatus, UserNotifySettings


class UserHelper:
    @staticmethod
    def __get_user_by_telegram_id(user_telegram_id: int) -> UserStatus:
        user = UserStatus.find_one(user_telegram_id=user_telegram_id)
        if user is None:
            raise DatabaseException(
                f'User with telegram id {user_telegram_id} not found in database'
            )

        return user

    @staticmethod
    def get_user_settings_by_telegram_id(
        user_telegram_id: int,
    ) -> UserNotifySettings:
        user_notify_settings = UserNotifySettings.find_one(
            user_telegram_id=user_telegram_id
        )
        if user_notify_settings is None:
            raise DatabaseException(
                f'Settings of user with telegram id {user_telegram_id} not found in database'
            )

        return user_notify_settings

    @staticmethod
    def create_user_if_not_exist(user_telegram_id: int) -> None:
        existed_user = UserStatus.find_one(user_telegram_id=user_telegram_id)
        if existed_user is None:
            user = UserStatus()
            user.fill(user_telegram_id=user_telegram_id)
            user.save()

        existed_user_settings = UserNotifySettings.find_one(
            user_telegram_id=user_telegram_id
        )
        if existed_user_settings is None:
            user_settings = UserNotifySettings()
            user_settings.fill(user_telegram_id=user_telegram_id)
            user_settings.save()

    @classmethod
    def is_user_agreement_accepted(cls, user_telegram_id: int) -> bool:
        user = cls.__get_user_by_telegram_id(user_telegram_id=user_telegram_id)
        return user.agreement_accepted

    @classmethod
    def accept_user_agreement(cls, user_telegram_id: int) -> None:
        user = cls.__get_user_by_telegram_id(user_telegram_id=user_telegram_id)
        user.agreement_accepted = True
        user.save()

    @classmethod
    def is_user_orioks_authenticated(cls, user_telegram_id: int) -> bool:
        user = cls.__get_user_by_telegram_id(user_telegram_id=user_telegram_id)
        return user.authenticated

    @classmethod
    def get_login_attempt_count(cls, user_telegram_id: int) -> int:
        user = cls.__get_user_by_telegram_id(user_telegram_id=user_telegram_id)
        return user.login_attempt_count

    @classmethod
    def increment_login_attempt_count(cls, user_telegram_id: int) -> None:
        user = cls.__get_user_by_telegram_id(user_telegram_id=user_telegram_id)
        user.login_attempt_count += 1
        user.save()

    @classmethod
    def update_notification_settings(
        cls, user_telegram_id: int, setting_name: str
    ) -> None:
        user_settings = cls.get_user_settings_by_telegram_id(
            user_telegram_id=user_telegram_id
        )
        if getattr(user_settings, setting_name) is None:
            raise DatabaseException(
                f'Setting with name {setting_name} for user with id {user_telegram_id} not found'
            )

        setattr(
            user_settings,
            setting_name,
            not bool(getattr(user_settings, setting_name)),
        )
        user_settings.save()

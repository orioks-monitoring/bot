import logging

from aiohttp import ClientSession

from config import config


class LoginLogoutHelper:
    @staticmethod
    async def _create_session() -> ClientSession:
        return ClientSession(
            timeout=config.REQUESTS_TIMEOUT,
            headers={
                config.LOGIN_LOGOUT_SERVICE_HEADER_NAME: config.LOGIN_LOGOUT_SERVICE_TOKEN
            },
        )

    @classmethod
    async def make_login(
        cls, encrypted_cookies: dict[str, str], user_telegram_id: int
    ) -> None:
        logging.info(
            "Sending login request to login-logout service for user %s",
            user_telegram_id,
        )
        async with await cls._create_session() as http_session:
            async with http_session.patch(
                config.LOGIN_LOGOUT_SERVICE_URL_FOR_LOGIN.format(
                    user_telegram_id=user_telegram_id
                ),
                json={"cookies": encrypted_cookies},
            ) as service_response:
                logging.info(
                    "Response status from login-logout service: %s",
                    service_response.status,
                )
                logging.info(
                    "Response text from login-logout service: %s",
                    await service_response.text(),
                )
                service_response.raise_for_status()
        logging.info("Successfully sent login request to login-logout service")

    @classmethod
    async def make_logout(cls, user_telegram_id: int) -> None:
        logging.info(
            "Sending logout request to login-logout service for user %s",
            user_telegram_id,
        )
        async with await cls._create_session() as http_session:
            async with http_session.post(
                config.LOGIN_LOGOUT_SERVICE_URL_FOR_LOGOUT.format(
                    user_telegram_id=user_telegram_id
                ),
            ) as service_response:
                logging.info(
                    "Response status from login-logout service: %s",
                    service_response.status,
                )
                logging.info(
                    "Response text from login-logout service: %s",
                    await service_response.text(),
                )
                service_response.raise_for_status()
        logging.info(
            "Successfully sent logout request to login-logout service"
        )

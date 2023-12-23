import logging

from aiohttp import ClientSession
from yarl import URL

from config import config


class CookiesHelper:
    @staticmethod
    def encrypt_cookies_from_session(
        session: ClientSession, filter_by_url: URL
    ) -> dict[str, str]:
        logging.info("Encrypting cookies")
        cookies = session.cookie_jar.filter_cookies(filter_by_url)

        dict_of_cookies = {}
        for _, cookie in cookies.items():
            dict_of_cookies[cookie.key] = config.FERNET_CIPHER_SUITE.encrypt(
                cookie.coded_value.encode('utf-8')
            ).decode("utf-8")
        logging.info("Successfully encrypted cookies")
        return dict_of_cookies

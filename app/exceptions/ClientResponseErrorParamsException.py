from aiohttp import ClientResponseError


class ClientResponseErrorParamsException(ClientResponseError):
    def __init__(self, *args, user_telegram_id: int | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_telegram_id = user_telegram_id

    def __str__(self) -> str:
        return f"{super().__str__()}, user_telegram_id={self.user_telegram_id}"

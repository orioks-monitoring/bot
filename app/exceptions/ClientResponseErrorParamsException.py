from aiohttp import ClientResponseError


class ClientResponseErrorParamsException(ClientResponseError):
    def __init__(
        self,
        *args,
        user_telegram_id: int | None = None,
        raw_html: str | None = None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.user_telegram_id = user_telegram_id
        self.raw_html = raw_html

    def __str__(self) -> str:
        return f"{super().__str__()}, user_telegram_id={self.user_telegram_id}"

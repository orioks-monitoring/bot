from aiohttp import ClientSession


class ClientSessionHelper(ClientSession):
    """
    Class with the same interface as aiohttp.ClientSession. The only difference is that it has an additional parameter.
    """

    def __init__(
        self, *args, user_telegram_id: int | None = None, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.user_telegram_id = user_telegram_id

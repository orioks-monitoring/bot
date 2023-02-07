import secrets
from pathlib import Path

from app.exceptions import ClientResponseErrorParamsException
from app.helpers import StorageHelper, TelegramMessageHelper, CommonHelper


class ClientResponseErrorParamsExceptionHelper:
    @staticmethod
    async def check(exception: ClientResponseErrorParamsException) -> None:
        if exception.raw_html:
            _filename = Path(
                f'{exception.user_telegram_id}_{secrets.token_hex(7)}.html'
            )
            try:
                await StorageHelper.save(
                    exception.raw_html, filename=_filename
                )
                await TelegramMessageHelper.document_to_admins(
                    message=f'Ошибка в запросах ОРИОКС!\n{exception}',
                    document_path=_filename,
                )
            finally:
                CommonHelper.safe_delete(_filename)
        else:
            await TelegramMessageHelper.message_to_admins(
                message=f'Ошибка в запросах ОРИОКС! (exception.raw_html is None)\n{exception}'
            )

import time

from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import CallbackQuery, Message
from prometheus_client import Counter, Histogram


class PrometheusMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        super().__init__()
        self.messages_total = Counter(
            "bot_messages_total", "Total messages", ["type", "user_telegram_id"]
        )
        self.responses_total = Counter(
            "bot_responses_total", "Total responses", ["handler"]
        )
        self.errors_total = Counter("bot_errors_total", "Total errors", ["handler"])
        self.processing_time = Histogram(
            "bot_handler_duration_seconds", "Handler duration", ["handler"]
        )

    async def on_pre_process_message(self, message: Message, data: dict) -> None:
        data["start_time"] = time.time()
        self.messages_total.labels(
            type="message",
            user_telegram_id=str(message.from_user.id),
        ).inc()

    async def on_post_process_message(
        self, message: Message, results, data: dict
    ) -> None:
        handler = data.get("handler_name", "unknown")
        self.responses_total.labels(handler=handler).inc()
        if "start_time" in data:
            duration = time.time() - data["start_time"]
            self.processing_time.labels(handler=handler).observe(duration)

    async def on_pre_process_callback_query(
        self, call: CallbackQuery, data: dict
    ) -> None:
        data["start_time"] = time.time()
        self.messages_total.labels(
            type="callback_query",
            user_telegram_id=str(call.from_user.id),
        ).inc()

    async def on_post_process_callback_query(
        self, call: CallbackQuery, results, data: dict
    ) -> None:
        handler = data.get("handler_name", "unknown")
        self.responses_total.labels(handler=handler).inc()
        if "start_time" in data:
            duration = time.time() - data["start_time"]
            self.processing_time.labels(handler=handler).observe(duration)

    async def on_process_message(self, message: Message, data: dict) -> None:
        if "handler" in data:
            data["handler_name"] = data["handler"].__name__

    async def on_process_callback_query(self, call: CallbackQuery, data: dict) -> None:
        if "handler" in data:
            data["handler_name"] = data["handler"].__name__

    async def on_post_process_error(self, update, exception, data: dict):
        handler = data.get("handler_name", "unknown")
        self.errors_total.labels(handler=handler).inc()

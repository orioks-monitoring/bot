import msgpack

from app.queue import Producer, Priority
from message_models.models import ToAdminsMessage


class MessageToAdminsHelper:
    @staticmethod
    async def send(message: str) -> None:
        msg = ToAdminsMessage(message=message)
        serialized_data = msgpack.packb(msg.model_dump())
        await Producer.send(
            serialized_data, queue_name="notifier", priority=Priority.HIGHEST
        )

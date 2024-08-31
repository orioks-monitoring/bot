import logging
from enum import IntEnum, unique
from time import time

import aio_pika
from aio_pika import DeliveryMode, Message

from config import config


@unique
class Priority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    VERY_HIGH = 4
    HIGHEST = 5


class Producer:
    @staticmethod
    async def send(message_body: bytes, queue_name: str, *, priority: int = 0) -> None:
        connection = await aio_pika.connect_robust(config.RABBIT_MQ_URL)

        async with connection:
            channel = await connection.channel()
            message = Message(
                message_body,
                delivery_mode=DeliveryMode.PERSISTENT,
                priority=priority,
                timestamp=time(),
            )
            await channel.default_exchange.publish(message, routing_key=queue_name)

            logging.info("Sent message to queue: %r", message)

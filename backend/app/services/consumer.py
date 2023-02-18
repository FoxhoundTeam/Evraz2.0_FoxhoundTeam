import asyncio
import json

from aiokafka import AIOKafkaConsumer, TopicPartition
from aiokafka.helpers import create_ssl_context
from loguru import logger

from app.config import settings
from app.database import Message
from app.services.message import MessageService


class Consumer:
    kc: AIOKafkaConsumer
    local_task: asyncio.Task

    def __init__(self):
        self.kc = AIOKafkaConsumer(
            settings.kafka_topic,
            bootstrap_servers=settings.kafka_server,
            security_protocol="SASL_SSL",
            sasl_mechanism="SCRAM-SHA-512",
            sasl_plain_username=settings.kafka_user,
            sasl_plain_password=settings.kafka_password,
            ssl_context=create_ssl_context(cafile="CA.pem"),
        )

    @property
    def message_service(self) -> MessageService:
        return MessageService()

    @property
    def topic(self) -> TopicPartition:
        return TopicPartition(settings.kafka_topic, 0)

    async def _seek_to_latest(self):
        logger.info("Seeking to latest")
        latest_message = await self.message_service.latest()
        offset = latest_message.offset + 1 if latest_message else 0
        if latest_message:
            logger.info(
                "Latest offset in db {latest_offset}",
                latest_offset=latest_message.offset,
            )
        self.kc.seek(self.topic, offset)
        logger.info("Sought to latest")

    async def _load_missed(self, batch_size=5_000):
        logger.info("Loading missed messages")
        await self._seek_to_latest()
        offsets = await self.kc.end_offsets([self.topic])
        last_offset = offsets[self.topic] - 1
        logger.info(
            "Latest message offset in kafka {last_offset}",
            last_offset=last_offset,
        )
        messages: list[Message] = []
        async for msg in self.kc:
            messages.append(
                Message(
                    offset=msg.offset,
                    message=json.loads(msg.value.decode("utf-8")),
                    dttm=msg.timestamp,
                )
            )
            if len(messages) >= batch_size:
                await self.message_service.batch_create(messages)
                messages = []
            if msg.offset >= last_offset:
                logger.info(f"Loaded missed messages till {msg.offset}")
                break
        await self.message_service.batch_create(messages)
        logger.info("Successfully loaded all missed messages")

    async def _consume(self):
        await self._load_missed()
        logger.info("Starting consuming")
        async for msg in self.kc:
            logger.info(f"Got message {msg.offset}")
            # TODO make predict here
            await self.message_service.create(
                msg.offset,
                json.loads(msg.value.decode("utf-8")),
                msg.timestamp,
            )

    async def _start(self):
        await self.kc.start()
        try:
            await self._consume()
        finally:
            await self.kc.stop()

    async def start(self):
        self.local_task = asyncio.create_task(self._start())

    async def stop(self):
        if self.local_task.done():
            self.local_task.result()
        else:
            self.local_task.cancel()

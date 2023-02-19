import asyncio
import json
from datetime import datetime

from aiokafka import AIOKafkaConsumer, TopicPartition
from aiokafka.helpers import create_ssl_context
from dateparser import parse
from loguru import logger

from app.config import settings
from app.database import Message
from app.database.prediction import PredictionType
from app.predictor import Predictor
from app.services.message import MessageService
from app.services.prediction import PredictionService


class Consumer:
    kc: AIOKafkaConsumer
    local_task: asyncio.Task
    message_service: MessageService
    topic: TopicPartition
    predictor: Predictor
    latest_message_dttm: datetime
    prediction_service: PredictionService

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
        self.message_service = MessageService()
        self.topic = TopicPartition(settings.kafka_topic, 0)
        self.predictor = Predictor()
        self.prediction_service = PredictionService()

    async def _init_predictor_messages(self):
        logger.info("Initializing predictor")
        async for message in self.message_service.get_for_prediction(12):
            self.predictor.write_mes(message)
        self.latest_message_dttm = parse(message["moment"])
        logger.info(
            "Predictor initialization finished, total rows {rows}",
            rows=len(self.predictor.t),
        )
        await self._make_prediction(PredictionType.linear)
        await self._make_prediction(PredictionType.halt_winters)

    async def _make_prediction(self, prediction_type: PredictionType):
        logger.info(
            "Making prediction for {prediction_type}",
            prediction_type=prediction_type,
        )
        loop = asyncio.get_event_loop()
        if prediction_type == PredictionType.linear:
            await loop.run_in_executor(None, self.predictor.fit_linear, 10)
            prediction = await loop.run_in_executor(None, self.predictor.predict_linear)
        else:
            await loop.run_in_executor(None, self.predictor.fit_halt_winters, 10)
            prediction = await loop.run_in_executor(None, self.predictor.predict_hw)
        for bearing_num, (
            expires_days,
            expires_error_days,
            reason,
        ) in prediction.items():
            logger.info("Got prediction for {num}", num=bearing_num)
            await self.prediction_service.update_or_create(
                bearing_num,
                expires_days,
                expires_error_days,
                reason,
                prediction_type,
                exhauster=0,
            )
        logger.info("Prediction finished")

    async def _add_predictor_message(self, message: Message):
        dttm = message.dttm.replace(tzinfo=None)
        if (dttm - self.latest_message_dttm).total_seconds() >= 12 * 60:
            logger.info("Adds predictor message from {dttm}", dttm=dttm)
            self.latest_message_dttm = dttm
            self.predictor.write_mes(message.message)
            await self._make_prediction(PredictionType.linear)
            await self._make_prediction(PredictionType.halt_winters)

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
        await self._seek_to_latest()
        logger.info("Loading missed messages")
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
        await self._init_predictor_messages()
        logger.info("Starting consuming")
        async for msg in self.kc:
            logger.info(f"Got message {msg.offset}")
            data = json.loads(msg.value.decode("utf-8"))
            message = await self.message_service.create(
                msg.offset,
                data,
                data["moment"],
            )
            await self._add_predictor_message(message)

    async def _start(self):
        await self.kc.start()
        try:
            await self._consume()
        except Exception as e:
            logger.exception("Error in consumer {e}", e=e)
        finally:
            await self.kc.stop()

    async def start(self):
        self.local_task = asyncio.create_task(self._start())

    async def stop(self):
        if self.local_task.done():
            self.local_task.result()
        else:
            self.local_task.cancel()

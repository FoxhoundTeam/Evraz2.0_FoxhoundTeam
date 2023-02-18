from datetime import datetime

from fastapi import HTTPException, status

from app.config import settings
from app.database import Message


class MessageService:
    async def create(
        self, offset: int, message: dict, dttm: datetime | None = None
    ) -> Message:
        return await Message(offset=offset, message=message, dttm=dttm).save()

    async def latest(self) -> Message | None:
        return await Message.find_all().sort(-Message.dttm).first_or_none()

    async def all(self, dttm_from: datetime, dttm_to: datetime | None) -> list[Message]:
        dttm_to = dttm_to or datetime.utcnow()
        if (dttm_to - dttm_from).total_seconds() > settings.max_history_delta:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Max delta for history is {settings.max_history_delta} seconds",
            )

        return await Message.find(
            Message.dttm >= dttm_from, Message.dttm <= dttm_to
        ).to_list()

    async def batch_create(self, messages: list[Message]):
        await Message.insert_many(messages)

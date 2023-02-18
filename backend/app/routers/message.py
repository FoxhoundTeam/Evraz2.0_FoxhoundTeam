from datetime import datetime

from fastapi import APIRouter, Depends

from app.database import Message
from app.services.message import MessageService

router = APIRouter(
    prefix="/message",
    tags=["message"],
)


@router.get(
    "/",
    response_model=list[Message],
    response_model_by_alias=False,
    description="Получить все сообщения с определенной даты",
)
async def get_messages(
    dttm_from: datetime,
    dttm_to: datetime | None = None,
    message_service: MessageService = Depends(),
):
    return await message_service.all(dttm_from, dttm_to)


@router.get(
    "/latest/",
    response_model=Message,
    response_model_by_alias=False,
    description="Получить последнее сообщение",
)
async def get_latest_message(message_service: MessageService = Depends()):
    return await message_service.latest()

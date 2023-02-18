from datetime import datetime

from beanie import Document, Indexed
from pydantic import Field


class Message(Document):
    offset: int
    message: dict
    dttm: Indexed(datetime) = Field(default_factory=lambda: datetime.utcnow())

    class Settings:
        name = "messages"

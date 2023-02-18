import motor.motor_asyncio
from beanie import init_beanie

from app.config import settings
from app.database.message import Message


async def init_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(settings.database_uri)

    await init_beanie(
        database=getattr(client, settings.mongodb_db), document_models=[Message]
    )

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import init_db
from app.routers import router
from app.services.consumer import Consumer

app = FastAPI(title=settings.project_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)

global_consumer = Consumer()


@app.on_event("startup")
async def start_db():
    await init_db()


@app.on_event("startup")
async def start_consumer():
    await global_consumer.start()


@app.on_event("shutdown")
async def stop_consumer():
    await global_consumer.stop()

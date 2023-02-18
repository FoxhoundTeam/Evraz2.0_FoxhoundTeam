from fastapi import APIRouter

from . import message, prediction

router = APIRouter(prefix="/api")
router.include_router(message.router)
router.include_router(prediction.router)

from fastapi import APIRouter, Depends

from app.database import Prediction
from app.database.prediction import PredictionType
from app.services.prediction import PredictionService

router = APIRouter(
    prefix="/prediction",
    tags=["prediction"],
)


@router.get(
    "/",
    response_model=list[Prediction],
    response_model_by_alias=False,
    description="Получить все прогнозы даты отказа",
)
async def get_predictions(
    prediction_service: PredictionService = Depends(),
):
    return await prediction_service.all()


@router.get(
    "/{exhauster}/{bearing_num}/",
    response_model=Prediction,
    response_model_by_alias=False,
    description="Получить прогноз для определенного подшипника эксгаустера",
)
async def get_prediction(
    exhauster: int,
    bearing_num: int,
    prediction_type: PredictionType = PredictionType.linear,
    prediction_service: PredictionService = Depends(),
):
    return await prediction_service.get(bearing_num, prediction_type, exhauster)

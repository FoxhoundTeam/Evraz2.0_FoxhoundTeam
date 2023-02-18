from datetime import datetime, timedelta

from fastapi import HTTPException, status

from app.database import Prediction
from app.database.prediction import PredictionType


class PredictionService:
    async def all(self) -> list[Prediction]:
        return await Prediction.all().to_list()

    async def get(self, bearing_num: int) -> Prediction:
        prediction = await Prediction.find_one(Prediction.bearing_num == bearing_num)
        if prediction is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Prediction with such bearing_num not found.",
            )
        return prediction

    async def update_or_create(
        self,
        bearing_num: int,
        expires_days: int,
        expires_error_days: int,
        reason: str,
        prediction_type: PredictionType,
    ) -> Prediction:
        prediction = await Prediction.find_one(
            Prediction.bearing_num == bearing_num,
            Prediction.prediction_type == prediction_type,
        )
        expires_at = datetime(2022, 1, 1) + timedelta(days=expires_days)
        if prediction is not None:
            prediction.expires_at = expires_at
            prediction.expires_error_days = int(expires_error_days)
            prediction.reason = reason
            await prediction.save()
        else:
            prediction = await Prediction(
                bearing_num=bearing_num,
                expires_at=expires_at,
                expires_error_days=int(expires_error_days),
                reason=reason,
                prediction_type=prediction_type,
            ).save()
        return prediction

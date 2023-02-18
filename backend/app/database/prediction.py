from datetime import datetime
from enum import Enum

from beanie import Document


class PredictionType(str, Enum):
    linear = "linear"
    halt_winters = "halt_winters"


class Prediction(Document):
    bearing_num: int
    expires_at: datetime
    expires_error_days: int
    reason: str
    prediction_type: PredictionType

    class Settings:
        name = "predictions"

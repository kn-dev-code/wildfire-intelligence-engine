from pydantic import BaseModel
from datetime import date


class FirePredictionRequest(BaseModel):
  west_longitude: float
  south_latitude: float
  east_longitude: float
  north_latitude: float


class FireDataResponse(BaseModel):
  latitude: float
  longitude: float
  brightness: float
  frp: float
  acq_date: date
  acq_time: int
  confidence: bool
  daynight: str
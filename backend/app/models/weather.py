from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime



class WeatherRecord(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    location_name: str
    temperature: float
    humidity: float
    wind_speed: float
    vpd: float
    timestamp: datetime
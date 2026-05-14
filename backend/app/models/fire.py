from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class FireRecord(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    latitude: float
    longitude: float
    fire_power: float
    acquired_date: datetime
    confidence: str
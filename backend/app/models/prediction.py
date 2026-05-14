from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class PredictionRecord(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    region_boundary: str
    risk_score: float
    prediction_type: str
    generated_at: datetime
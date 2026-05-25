from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from app.schemas.weather_schema import WeatherQuery
from app.controllers.weather_controller import query_weather_controller
from app.core.database import get_db 
from app.core.security import get_current_user_from_cookie

weather_router = APIRouter()

@weather_router.post("/current", status_code=status.HTTP_200_OK)
def get_current_weather(
    weather_data: WeatherQuery, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_cookie)
):
    return query_weather_controller(
        user_id=current_user.id, 
        weather_data=weather_data, 
        db=db
    )
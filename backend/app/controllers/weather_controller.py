from fastapi import status, HTTPException
from sqlmodel import Session, select
from app.models.weather import WeatherRecord
from app.schemas.weather_schema import WeatherQuery
from app.controllers.fire_controller import _verify_active_user
from app.api.weather_api import base_url, weather_api
import requests


def query_weather_controller(user_id: int, weather_data: WeatherQuery, db: Session):
  _verify_active_user(user_id, db)

  lat = weather_data.latitude
  lon = weather_data.longitude

  weather_url = f"{base_url}?lat={lat}&lon={lon}&appid={weather_api}&units=metric"



from fastapi import status, HTTPException
from sqlmodel import Session
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

  response = requests.get(weather_url)

  if response.status_code != 200: 
    raise HTTPException(
      status_code = status.HTTP_400_BAD_REQUEST,
      detail = "Bad Request. Please try again."
    )

  data = response.json()

  temp = data["main"]["temp"]
  humidity = data["main"]["humidity"]
  wind_speed = data["main"].get("speed", 0.0)
  svp = 0.61078 * (10 ** ((7.5 * temp) / (237.3 + temp)))
  vpd = svp * (1 - (humidity / 100))

  return {
        "status": "success",
        "message": "Weather data retrieved successfully",
        "data": {
            "temperature": temp,
            "humidity": humidity,
            "wind_speed": wind_speed,
            "vpd": round(vpd, 3), 
            "location": data.get("name", "Unknown Location")
        }
    }
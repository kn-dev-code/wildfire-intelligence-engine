from fastapi import status, HTTPException
from sqlmodel import Session
from app.controllers.fire_controller import _verify_active_user
from app.schemas.intelligence_schema import FireDataResponse, FirePredictionRequest
from app.api.nasa_api import base_url, nasa_api
import requests


def query_intelligence_controller(user_id: int, prediction_request: FirePredictionRequest, db: Session):
  _verify_active_user(user_id, db)
  west_lon = prediction_request.west_longitude
  south_lat = prediction_request.south_latitude
  east_lon = prediction_request.east_longitude
  north_lat = prediction_request.north_latitude
  source = "VIIRS_NOAA20_NRT"
  day_range = 1
  prediction_url = f"{base_url}/api/area/{nasa_api}/{source}/{west_lon},{south_lat},{east_lon},{north_lat}/{day_range}"
  try:
      response = requests.get(prediction_url)
      response.raise_for_status()
  except requests.exceptions.RequestException as e:
      raise HTTPException(
        status_code = status.HTTP_503_SERVICE_UNAVAILABLE,
        detail = f"NASA FIRMS service unreachable: {str(e)}"
      )
  data = response.json()

  return {
    "status": "success",
    "message": "Thermal hotspots retrieved successfully",
    "hotspots_found": len(data),
    "data": data
  }
  
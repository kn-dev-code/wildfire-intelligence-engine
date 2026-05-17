from fastapi import FastAPI
from fastapi import APIRouter
from app.routes.fire_router import fire_router
from app.routes.weather import weather_router
from app.routes.intelligence_router import intelligence_router


main_router = APIRouter()




main_router.include_router(fire_router, prefix="/api/v1/fires")
main_router.include_router(weather_router, prefix="/api/v1/weather")
main_router.include_router(intelligence_router, prefix="/api/v1/intelligence")

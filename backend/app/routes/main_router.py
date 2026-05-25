from fastapi import FastAPI
from fastapi import APIRouter
from app.routes.fire_router import fire_router
from app.routes.weather_router import weather_router
from app.routes.intelligence_router import intelligence_router
from app.routes.user_router import user_router

main_router = APIRouter()



main_router.include_router(user_router, prefix="/api/v1/users", tags=["Users"])
main_router.include_router(fire_router, prefix="/api/v1/fires", tags= ["Fires"])
main_router.include_router(weather_router, prefix="/api/v1/weather", tags = ["Weather"])
main_router.include_router(intelligence_router, prefix="/api/v1/intelligence", tags = ["Intelligence"])

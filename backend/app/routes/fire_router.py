from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.core.database import get_db
from app.schemas.fire_schema import FireUpdate
from app.controllers.fire_controller import (
    read_fire_controller,
    get_all_fire_reports_controller,
    update_fire_report_controller,
    delete_fire_report_controller
)

fire_router = APIRouter()

@fire_router.get("")
def get_all_fires(db: Session = Depends(get_db)):
    return get_all_fire_reports_controller(db)

@fire_router.get("/{fire_id}")
def get_single_fire(fire_id: int, db: Session = Depends(get_db)):
    return read_fire_controller(fire_id, db)

@fire_router.patch("/{fire_id}")
def update_fire(fire_id: int, fire_data: FireUpdate, db: Session = Depends(get_db)):
    return update_fire_report_controller(fire_id, fire_data, db)

@fire_router.delete("/{fire_id}")
def delete_fire(fire_id: int, db: Session = Depends(get_db)):
    return delete_fire_report_controller(fire_id, db)
from fastapi import Response, HTTPException, status
from sqlmodel import Session, select
from app.models.user import UserRecord
from app.schemas.fire_schema import FireCreate, FireUpdate 
from app.models.fire import FireRecord

def _verify_active_user(user_id: int, db: Session) -> UserRecord:
    """Internal helper to authenticate and validate the user's status."""
    user = db.exec(select(UserRecord).where(UserRecord.id == user_id)).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User executing this action was not found"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This account is inactive and cannot perform this action"
        )
    return user


def report_fire_controller(user_id: int, fire_data: FireCreate, db: Session):
    _verify_active_user(user_id, db)

    db_fire = FireRecord(
        latitude=fire_data.latitude,
        longitude=fire_data.longitude,
        fire_power=fire_data.fire_power,
        acquired_date=fire_data.acquired_date,
        confidence=fire_data.confidence,
        reported_by_id=user_id
    )

    db.add(db_fire)
    db.commit()
    db.refresh(db_fire)

    return {
        "status": "success",
        "message": "Wildfire data captured successfully",
        "data": db_fire
    }


def read_fire_controller(user_id: int, fire_id: int, db: Session):
    _verify_active_user(user_id, db)
  
    fire = db.get(FireRecord, fire_id)
    if not fire:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Fire report with ID {fire_id} not found"
        )
  
    return {"status": "success", "data": fire}
  

def get_all_fire_reports_controller(user_id: int, db: Session):
    _verify_active_user(user_id, db)
  
    statement = select(FireRecord)
    fires = db.exec(statement).all()

    return {"status": "success", "count": len(fires), "data": fires}


def update_fire_report_controller(fire_id: int, user_id: int, fire_data: FireUpdate, db: Session):
    _verify_active_user(user_id, db)

    db_fire = db.get(FireRecord, fire_id)
    if not db_fire:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Fire report with ID {fire_id} not found"
        )
        
    update_dict = fire_data.model_dump(exclude_unset=True)

    for key, value in update_dict.items():
        setattr(db_fire, key, value)
  
    db.add(db_fire)
    db.commit()
    db.refresh(db_fire)
    return {"status": "success", "data": db_fire}


def delete_fire_report_controller(user_id: int, fire_id: int, db: Session):
    _verify_active_user(user_id, db)
  
    db_fire = db.get(FireRecord, fire_id)
    if not db_fire:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Fire report with ID {fire_id} not found"
        )
        
    db.delete(db_fire)
    db.commit()
    return {"status": "success", "message": f"Fire report {fire_id} successfully deleted"}
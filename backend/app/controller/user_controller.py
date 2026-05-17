from fastapi import HTTPException, status
from sqlmodel import Session, select
from app.models.user import UserRecord 
from app.schemas.user_schema import UserCreate, UserLogin

def create_user_controller(user_data: UserCreate, db: Session):
   
    simulated_hash = f"hashed_version_of_{user_data.password}" 

    db_user = UserRecord(
        username=user_data.username,
        email=user_data.email,
        hashed_password=simulated_hash, 
        is_active=True 
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return {"status": "success", "data": db_user}


def login_user_controller(user_data: UserLogin, db: Session):
    
    find_user = select(UserRecord).where(UserRecord.email == user_data.email)
    user = db.exec(find_user).first()


    if not user:
        raise HTTPException(
            status_code = status.HTTP_401.UNAUTHORIZED,
            detail = "Invalid email or password"
        )
    
    simulated_valid = (f"hashed_version_of_{user_data.password}" == user.hashed_password)
    if not simulated_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
        
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This account has been deactivated"
        )

    return {
        "status": "success",
        "message": "Login successful",
        "token": "simulated-jwt-token-string", 
        "user": {
            "username": user.username,
            "email": user.email,
            "role": user.role
        }
    }
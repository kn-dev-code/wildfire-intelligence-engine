from fastapi import HTTPException, status, Response
from sqlmodel import Session, select
from app.models.user import UserRecord 
from app.schemas.user_schema import UserCreate, UserLogin
from app.core.security import verify_password, create_access_token

def create_user_controller(register_data: UserCreate, db: Session):
   
    simulated_hash = f"hashed_version_of_{register_data.password}" 

    db_user = UserRecord(
        username=register_data.username,
        email=register_data.email,
        hashed_password=simulated_hash, 
        is_active=True 
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return {"status": "success", "data": db_user}


def login_user_controller(login_data: UserLogin, response: Response, db: Session):
    
    find_user = select(UserRecord).where(UserRecord.email == login_data.email)
    user = db.exec(find_user).first()


    if not user or not user.is_active:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid email or password"
        )
    
    if not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
        
    token_payload = {"sub": str(user.id), "email": user.email, "role": user.role}
    token = create_access_token(data=token_payload)

    response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,
            samesite="lax",
            secure=True,
            max_age=3600
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

def update_user_controller(user_id: int, user_data: UserCreate, db: Session):
    find_user = select(UserRecord).where(UserRecord.id == user_id)

    user = db.exec(find_user).first()

    if not user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid email or password"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "This account has been deactivated"
        )
    user.username = user_data.username
    user.email = user_data.email
    user.hashed_password = f"hashed_version_of_{user_data.password}"


    db.add(user)
    db.commit()
    db.refresh(user)

def delete_user_controller(user_id: int, db:Session):
    user = db.get(UserRecord, user_id)


    if not user:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "User does not exist"
        )

    db.delete(user)
    db.commit()

    return {"status": "success", "message": "Account permanently deleted"}
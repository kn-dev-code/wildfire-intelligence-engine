from fastapi import HTTPException, status, Response, Request
from sqlmodel import Session, select
import os
import jwt
from dotenv import load_dotenv
from app.models.user import UserRecord 
from app.schemas.user_schema import UserCreate, UserLogin, TokenBody, GoogleAuthRequest
from app.core.security import verify_password, create_access_token, get_current_user_from_cookie, hash_password
from app.core.config import Settings


def create_user_controller(register_data: UserCreate, db: Session):
   
    hashed_code = hash_password(register_data.password)

    db_user = UserRecord(
        username=register_data.username,
        email=register_data.email,
        hashed_password=hashed_code, 
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
        "token": token, 
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
    user.hashed_password = hash_password(user_data.password)


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

async def google_auth_controller(google_credential: GoogleAuthRequest, response: Response, db: Session):
    load_dotenv()
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    try:

        google_user = jwt.decode(google_credential.token_str, options={"verify_signature":False})
        if google_user["aud"] != client_id: 
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Token mismatch")
    
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Invalid Google Token payload")

    email = google_user.get("email")
    username = google_user.get("name", email.split("@")[0])

    find_user = select(UserRecord).where(UserRecord.email == email)
    user = db.exec(find_user).first()
    if not user:
        user = UserRecord(
            username=username,
            email=email,
            hashed_password="OAUTH_USER_NO_PASSWORD", 
            is_active=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="This account has been deactivated")

    session_data = TokenBody(username=user.username, email=user.email, role=user.role)
    system_token = create_access_token(data=session_data.model_dump())
    response.set_cookie(
        key="access_token",
        value=system_token,
        httponly=True,
        samesite="lax",
        secure=True,
        max_age=900
    )

    return {
        "status": "success",
        "message": "Google ID Token authentication successful",
        "user": session_data
    }

def get_user_controller(request: Request, db: Session):
    
    token_payload = get_current_user_from_cookie(request)
    if not token_payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
        
    user_id = token_payload.get("sub")
    
    try:
        find_user = select(UserRecord).where(UserRecord.id == int(user_id))
        user = db.exec(find_user).first()
    except Exception as db_error:
        print(f"Database Error: {db_error}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Database Error")

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
    return {
        "status": "success",
        "message": "User data retrieved successfully",
        "user": {
            "username": user.username,
            "role": user.role,
            "is_active": user.is_active,
        }
    }
from fastapi import HTTPException, status, Response, Request, Body
from sqlmodel import Session, select
import os
import jwt
from dotenv import load_dotenv
from app.models.user import UserRecord 
from app.schemas.user_schema import UserCreate, UserLogin, TokenBody, GoogleAuthRequest
from app.core.security import verify_password, create_access_token, get_current_user_from_cookie, hash_password
from app.core.config import Settings

# Environment gate helper
IS_DEVELOPMENT = os.getenv("ENVIRONMENT", "development") == "development"
def create_user_controller(register_data: UserCreate, response: Response, db: Session):
    try:
        hashed_code = hash_password(register_data.password)
        fallback_username = register_data.username if register_data.username else register_data.email.split("@")[0]
        db_user = UserRecord(
            username=fallback_username,
            email=register_data.email,
            hashed_password=hashed_code, 
            is_active=True 
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        token_payload = {"sub": str(db_user.id), "email": db_user.email, "role": db_user.role}
        token = create_access_token(data=token_payload)
        
        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,
            samesite="lax",
            secure=False,
            max_age=3600
        )
        
        return {
            "status": "success",
            "message": "Registration and login successful",
            "token": token, 
            "user": {
                "username": db_user.username,
                "email": db_user.email,
                "role": db_user.role
            }
        }
    except Exception as e:
        print(f"\n[CREATE USER ERROR]: {str(e)}\n", flush=True)
        raise HTTPException(status_code=500, detail=f"Registration processing failed: {str(e)}")


def login_user_controller(login_data: UserLogin, response: Response, db: Session):
    find_user = select(UserRecord).where(UserRecord.email == login_data.email)
    user = db.exec(find_user).first()

    if not user or not user.is_active:
        print(f"\n[LOGIN FAILED]: Target user record not found or flagged inactive for email: {login_data.email}\n", flush=True)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    if not verify_password(login_data.password, user.hashed_password):
        print(f"\n[LOGIN FAILED]: Cryptographic check failed for email: {login_data.email}\n", flush=True)
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
        secure=False,
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
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User record modification authorized failed"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This account has been deactivated"
        )
        
    user.username = user_data.username
    user.email = user_data.email
    user.hashed_password = hash_password(user_data.password)

    db.add(user)
    db.commit()
    db.refresh(user)


def delete_user_controller(user_id: int, db: Session):
    user = db.get(UserRecord, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist"
        )

    db.delete(user)
    db.commit()
    return {"status": "success", "message": "Account permanently deleted"}


def google_auth_controller(google_credential: GoogleAuthRequest, response: Response, db: Session):
    load_dotenv()
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    try:
        google_user = jwt.decode(google_credential.token_str, options={"verify_signature": False})
        if google_user["aud"] != client_id: 
            print(f"\n[GOOGLE AUTH MISMATCH]: Expected audience client ID matching {client_id}, structural fallback triggered.\n", flush=True)
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token mismatch")
    
    except jwt.PyJWTError as jwt_err:
        print(f"\n[GOOGLE JWT EXCEPTION VALIDATION]: {str(jwt_err)}\n", flush=True)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid Google Token payload: {str(jwt_err)}")

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
    token_payload = {"sub": str(user.id), "username": session_data.username, "email": session_data.email, "role": session_data.role}
    system_token = create_access_token(data=token_payload)
    
    response.set_cookie(
        key="access_token",
        value=system_token,
        httponly=True,
        samesite="lax",
        secure=False,
        max_age=3600
    )

    return {
        "status": "success",
        "message": "Google ID Token authentication successful",
        "user": session_data
    }


def get_user_controller(request: Request, db: Session):
    print(f"\n[GET USER DEBUG]: Incoming Request Header Jar Metadata: {request.cookies}\n", flush=True)
    
    token_payload = get_current_user_from_cookie(request)
    if not token_payload:
        print("\n[GET USER INTERCEPTION]: Extraction step failed inside core utility wrapper module.\n", flush=True)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Cookie wrapper payload invalid or not provided")
        
    user_id = token_payload.get("sub")
    
    try:
        find_user = select(UserRecord).where(UserRecord.id == int(user_id))
        user = db.exec(find_user).first()
    except Exception as db_error:
        print(f"\n[GET USER PERSISTENCE DATABASE CRASH]: {str(db_error)}\n", flush=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Database Error")

    if not user:
        print(f"\n[GET USER RUNTIME VALIDATION MISMATCH]: User extraction validation returned null for active sub ID: {user_id}\n", flush=True)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Target user context missing from registry documentation")
        
    return {
        "status": "success",
        "message": "User data retrieved successfully",
        "user": {
            "username": user.username,
            "role": user.role,
            "is_active": user.is_active,
        }
    }
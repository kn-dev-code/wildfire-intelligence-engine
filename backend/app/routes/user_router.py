from fastapi import APIRouter, Depends, Response, Request
from sqlmodel import Session
from app.core.database import get_db
from app.controllers.user_controller import create_user_controller, login_user_controller, update_user_controller, delete_user_controller, google_auth_controller, get_user_controller
from app.schemas.user_schema import UserCreate, UserLogin, UserUpdate
from app.core.security import create_access_token, verify_password

user_router = APIRouter()


@user_router.post("/register")
def register(register_data: UserCreate, db: Session = Depends(get_db)):
  return create_user_controller(register_data, db)

@user_router.post("/login")
def login(login_data: UserLogin, response: Response, db:Session = Depends(get_db)):
  return login_user_controller(login_data, response, db)

@user_router.patch("/update")
def update(user_id: int, update_data: UserUpdate, db:Session = Depends(get_db)):
  return update_user_controller(user_id, update_data, db)

@user_router.delete("/delete/{user_id}")
def delete(user_id: int, response: Response, db:Session = Depends(get_db)):
  result = delete_user_controller(user_id, db)

  response.delete_cookie(
    key="access_token",
        httponly=True,
        samesite="lax",
        secure=True
  )

  return result

@user_router.post("/logout")
def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        httponly=True,
        samesite="lax",
        secure=True
    )
    return {"status": "success", "message": "Successfully logged out"}

@user_router.post("/google-auth")
def google_auth(code: str, state: str, response: Response, db: Session = Depends(get_db)):
  return google_auth_controller(code, state, response,  db)

@user_router.get("/get-user/me")
def get_user(request: Request, db: Session = Depends(get_db)):
  return get_user_controller(request=request, db=db)
from pydantic import BaseModel, EmailStr, Field, model_validator
from typing import Optional, Literal

class UserCreate(BaseModel):
  username: Optional[str] = None
  email: EmailStr
  password: str = Field(..., min_length=8)
  auth_provider: Literal["standard", "google"] = "standard"

  @model_validator(mode="after")
  def validate_auth(self) -> "UserCreate":
    if self.auth_provider == "standard" and self.password is None: 
      raise ValueError("Password is required for standard registration")
    if self.auth_provider == "google" and self.password is not None:
      raise ValueError("Password is not required for google registration")
    
    return self

class UserLogin(BaseModel):
  email: EmailStr
  password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
  username: Optional[str] = Field(None, min_length=3, max_length=20)
  email: Optional[EmailStr] = None
  password: Optional[str] = Field(default=None , min_length=8)


class GoogleAuthRequest(BaseModel):
  token_str: str


class TokenBody(BaseModel):
  username: Optional[str] = Field(None)
  email: Optional[EmailStr] = None
  role: str = "user"
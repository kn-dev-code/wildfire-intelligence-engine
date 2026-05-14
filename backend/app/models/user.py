from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class UserRecord(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str = Field(unique=True)
    hashed_password: str
    is_active: bool
    role: str = Field(default="user")
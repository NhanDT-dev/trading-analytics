from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict


class UserCreate(BaseModel):
    email: str
    password: str
    name: str


class UserUpdate(BaseModel):
    id: int
    email: str
    name: str


class ChangePassword(BaseModel):
    old_password: str
    new_password: str


class UserInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    name: str
    is_active: bool
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

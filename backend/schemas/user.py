from pydantic import BaseModel


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

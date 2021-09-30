from typing import Optional

from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class UserUpdate(BaseModel):
    full_name: str
    password: str


class User(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    disabled: Optional[bool] = False


class UserSignup(User):
    password: str


class UpdatePassword(BaseModel):
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserInDB(User):
    hashed_password: str

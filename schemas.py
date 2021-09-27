from pydantic import BaseModel, EmailStr
from typing import Optional


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


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

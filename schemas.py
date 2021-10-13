from typing import Literal, Optional

from pydantic import BaseModel, EmailStr, HttpUrl


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class UserUpdate(BaseModel):
    full_name: str
    profile_pic_url: HttpUrl
    gender: Literal['male', 'female', 'prefer not to say']
    email: EmailStr


class User(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    disabled: Optional[bool] = False
    gender: Literal['male', 'female', 'prefer not to say']


class UserSignup(User):
    password: str
    profile_pic_url: HttpUrl


class UserDisplay(User):
    profile_pic_url: HttpUrl


class UpdatePassword(BaseModel):
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserInDB(User):
    hashed_password: str
    profile_pic_url: HttpUrl

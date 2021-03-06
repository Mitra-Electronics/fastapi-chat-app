from typing import Literal, Optional

from pydantic import BaseModel, EmailStr, HttpUrl


class Token(BaseModel):
    access_token: str
    token_type: str
    sucess: Optional[bool]


class TokenData(BaseModel):
    email: Optional[EmailStr] = None


class UserUpdate(BaseModel):
    full_name: str
    profile_pic_url: HttpUrl
    gender: Literal['male', 'female', 'prefer not to say']
    email: EmailStr
    recovery_email: EmailStr


class UserDisplay(BaseModel):
    email: EmailStr
    full_name: str
    disabled: Optional[bool] = False
    gender: Literal['male', 'female', 'prefer not to say']
    profile_pic_url: HttpUrl


class User(UserDisplay):
    recovery_email: EmailStr


class UserSignup(BaseModel):
    email: EmailStr
    full_name: str
    gender: Literal['male', 'female', 'prefer not to say']
    profile_pic_url: HttpUrl
    recovery_email: EmailStr
    password: str


class UpdatePassword(BaseModel):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserInDB(User):
    hashed_password: str
    joining_date: str
    is_admin: bool
    is_superuser: bool

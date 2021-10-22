from datetime import datetime, timedelta

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic.networks import EmailStr, HttpUrl
from datetime import datetime

from config import (ALGORITHM, CREDENTIALS_EXCEPTION, DEPRECATED,
                    INACTIVE_EXCEPTION, LOGIN_FORM_TITLE, PEPPER, SCHEMES,
                    SECRET_KEY, TOKEN_TEST_URL, USER_DISABLED_TEXT, EMAIL_EXISTS_TEXT)
from drivers.mongodb_driver import delete, insert__, update_password, update_user_in_db__, get_user
from schemas import TokenData, User, UserInDB, UserSignup, UserUpdate

pwd_context = CryptContext(schemes=SCHEMES, deprecated=DEPRECATED)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=TOKEN_TEST_URL, scheme_name=LOGIN_FORM_TITLE)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


def authenticate_user(email: EmailStr, password: str):
    user = get_user(email)
    if not user:
        return False
    if not verify_password(password+PEPPER, user.hashed_password):
        return False
    if user.disabled:
        return USER_DISABLED_TEXT
    return user


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise CREDENTIALS_EXCEPTION
        token_data = TokenData(email=username)
    except JWTError:
        raise CREDENTIALS_EXCEPTION
    user = get_user(token_data.email)
    if user is None:
        raise CREDENTIALS_EXCEPTION
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise INACTIVE_EXCEPTION
    return current_user


def register_user(user: UserSignup, url: HttpUrl,gender: str) -> bool:
    if not get_user(user.email):
        insert__(get_password_hash(
            user.password+PEPPER), user.full_name, user.email, url, gender, user.recovery_email)
        return True
    else:
        return False


def change_password(email: EmailStr, updated_password: str):
    if get_user(email):
        update_password(email, get_password_hash(
            updated_password+PEPPER))

        return True
    else:
        return False


def change_user_in_db(email: str, update: UserUpdate):
    if get_user(email):
        if update_user_in_db__(email, update) is True:
            return True
        else: 
            return EMAIL_EXISTS_TEXT
    else:
        return False


def delete_user(user: UserInDB):
    if get_user(user.email):
        delete(user)
        return True
    else:
        return False

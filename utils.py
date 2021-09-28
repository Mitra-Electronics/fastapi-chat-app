from datetime import datetime, timedelta

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from config import (ALGORITHM, CREDENTIALS_EXCEPTION, DEPRECATED,
                    INACTIVE_EXCEPTION, LOGIN_FORM_TITLE, PEPPER, SCHEMES,
                    SECRET_KEY, TOKEN_TEST_URL, USER_DISABLED_TEXT)
from mongodb_driver import delete, fake_users_db__, insert__, update_password
from schemas import TokenData, User, UserInDB, UserSignup

pwd_context = CryptContext(schemes=SCHEMES, deprecated=DEPRECATED)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=TOKEN_TEST_URL, scheme_name=LOGIN_FORM_TITLE)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


def get_user(db: fake_users_db__, username: str, email=None):
    if email is None:
        search = {"username": username}
    else:
        search = {"username": username, "email": email}
    search = list(db.find(search))
    if search != []:
        user_dict = search[0]
        return UserInDB(**user_dict)


def authenticate_user(fake_db: fake_users_db__, username: str, password: str):
    user = get_user(fake_db, username)
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
        token_data = TokenData(username=username)
    except JWTError:
        raise CREDENTIALS_EXCEPTION
    user = get_user(fake_users_db__, username=token_data.username)
    if user is None:
        raise CREDENTIALS_EXCEPTION
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise INACTIVE_EXCEPTION
    return current_user


def register_user(fake_db: fake_users_db__, user: UserSignup) -> bool:
    if not get_user(fake_db, user.username, user.email):
        insert__(user.username, get_password_hash(
            user.password+PEPPER), user.full_name, user.email)
        return True
    else:
        return False


def change_password(fake_db: fake_users_db__, username: str, email: str, updated_password: str):
    if get_user(fake_db, username, email):
        update_password(username, email, get_password_hash(
            updated_password+PEPPER))

        return True
    else:
        return False


def delete_user(db: fake_users_db__, user: UserInDB):
    if get_user(db, user.username, user.email):
        delete(user)
        return True
    else:
        return False


from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pymongo import MongoClient

from config import ALGORITHM, PEPPER, SCHEMES, SECRET_KEY, TOKEN_URL, DEPRECATED
from mongodb_driver import fake_users_db__
from schemas import TokenData, User, UserInDB

pwd_context = CryptContext(schemes=SCHEMES, deprecated=DEPRECATED)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=TOKEN_URL)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


def get_user(db: MongoClient, username: str):
    search = list(db.find({"username": username}))
    if search != []:
        user_dict = search[0]
        return UserInDB(**user_dict)


def authenticate_user(fake_db: MongoClient, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password+PEPPER, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db__, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def register_user(fake_db: MongoClient, username: str, password: str, email: str, full_name: str) -> bool:
    if not get_user(fake_db, username):
        fake_db.insert_one({
            "username": username,
            "full_name": full_name,
            "email": email,
            "hashed_password": get_password_hash(password+PEPPER),
            "disabled": False,
        })
        return True
    else:
        return False


def change_password(fake_db: MongoClient, username: str, update_password: str):
    if get_user(fake_db, username):
        fake_db.update_one({"username": username}, {"$set": {"hashed_password": get_password_hash(
            update_password+PEPPER)}})
        return True
    else:
        return False


def delete_user():
    pass

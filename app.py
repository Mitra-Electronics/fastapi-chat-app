from datetime import timedelta

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from config import ACCESS_TOKEN_EXPIRE_MINUTES, TOKEN_URL
from schemas import Token, UserSignup
from utils import *

app = FastAPI()

# to get a string like this run:
# openssl rand -hex 32


@app.post("/"+TOKEN_URL, response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login"""
    user = authenticate_user(
        fake_users_db__, form_data.username, form_data.password)
    if not user:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},

        )
    if user == 'Disabled':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is disabled",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(

        data={"sub": user.username}, expires_delta=access_token_expires

    )

    return JSONResponse({"access_token": access_token, "token_type": "bearer"})


@app.post("/register", response_model=Token)
async def register_user_(user: UserSignup):
    user_create = register_user(
        fake_users_db__, user.username, user.password, user.email, user.full_name)
    if user_create is True:
        user = authenticate_user(
            fake_users_db__, user.username, user.password)
        if not user:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},

            )

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(

            data={"sub": user.username}, expires_delta=access_token_expires

        )

        return JSONResponse({"access_token": access_token, "token_type": "bearer"})
    else:
        raise HTTPException(
            status_code=status.HTTP_306_RESERVED,
            detail="User already exists",
            headers={"WWW-Authenticate": "Bearer"},
        )


@app.post("/users/me/change-password")
async def change_password_of_user(update: str, current_user: User = Depends(get_current_active_user)):
    user_update = change_password(
        fake_users_db__, current_user.username, update)
    if user_update is True:
        return {"status": "ok", "updated": True}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist",
            headers={"WWW-Authenticate": "Bearer"},
        )


@app.post("/users/me/delete-user")
async def delete_user(current_user: User = Depends(get_current_active_user)):
    user_delete = 0
    return JSONResponse({"status": "ok", "deleted": True})


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]

from fastapi import APIRouter, Depends, status, HTTPException
from utils import get_current_active_user, delete_user, change_user_in_db, change_password
from fastapi.responses import JSONResponse
from schemas import UserUpdate, User, UpdatePassword
from crud.recovery_crud import verify as verify_
from config import USERS_ME_TAGS, EMAIL_EXISTS_TEXT

me = APIRouter(tags=USERS_ME_TAGS)

@me.post("/change")
async def change_user(user: UserUpdate, current_user: User = Depends(get_current_active_user)):
    user_update = change_user_in_db(
        current_user.email, user)
    if user_update is True:
        return {"status": "ok", "updated": True}
        
    elif user_update is EMAIL_EXISTS_TEXT:
        raise HTTPException(
            status_code=status.HTTP_226_IM_USED,
            detail="Email is used",
            headers={"WWW-Authenticate": "Bearer"},
        )

    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist",
            headers={"WWW-Authenticate": "Bearer"},
        )

@me.get("/verify")
async def verify(token: str):
    verify_(token)
    return {"sucess":True}

@me.post("/delete-user")
async def delete_user_(current_user: User = Depends(get_current_active_user)):
    user_update = delete_user(current_user)
    if user_update is True:
        return JSONResponse({"status": "ok", "deleted": True})
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist",
            headers={"WWW-Authenticate": "Bearer"},
        )


@me.get("/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@me.post("/change-password")
async def change_password_of_user(update: UpdatePassword, current_user: User = Depends(get_current_active_user)):
    user_update = change_password(
        current_user.email, update.password)
    if user_update is True:
        return {"status": "ok", "updated": True}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist",
            headers={"WWW-Authenticate": "Bearer"},
        )

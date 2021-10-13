from fastapi import APIRouter, Depends, status, HTTPException
from utils import get_current_active_user, delete_user, fake_users_db__, change_user_in_db, change_password
from fastapi.responses import JSONResponse
from schemas import UserDisplay, UserUpdate, User, UpdatePassword
from config import USERS_TAGS

route = APIRouter(tags=USERS_TAGS)

@route.post("/change")
async def change_user(user: UserUpdate, current_user: User = Depends(get_current_active_user)):
    user_update = change_user_in_db(
        fake_users_db__, current_user.username, current_user.email, user)
    if user_update is True:
        return {"status": "ok", "updated": True}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist",
            headers={"WWW-Authenticate": "Bearer"},
        )


@route.post("/delete-user")
async def delete_user_(current_user: User = Depends(get_current_active_user)):
    user_update = delete_user(fake_users_db__, current_user)
    if user_update is True:
        return JSONResponse({"status": "ok", "deleted": True})
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist",
            headers={"WWW-Authenticate": "Bearer"},
        )


@route.get("/", response_model=UserDisplay)
async def read_users_me(current_user: UserDisplay = Depends(get_current_active_user)):
    return current_user


@route.get("/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]

@route.post("/change-password")
async def change_password_of_user(update: UpdatePassword, current_user: User = Depends(get_current_active_user)):
    user_update = change_password(
        fake_users_db__, current_user.username, current_user.email, update.password)
    if user_update is True:
        return {"status": "ok", "updated": True}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist",
            headers={"WWW-Authenticate": "Bearer"},
        )
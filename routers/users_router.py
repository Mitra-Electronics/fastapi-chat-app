from fastapi import APIRouter
from schemas import UserDisplay
from config import USERS_TAGS, USERS_ME_PREFIX
from routers.users_me_router import me
from drivers.mongodb_driver import search_user_in_db
from typing import List

route = APIRouter(tags=USERS_TAGS)

route.include_router(me, prefix=USERS_ME_PREFIX)


@route.get("/search/", response_model=List[UserDisplay])
async def read_own_items(term: str):
    return search_user_in_db(term)

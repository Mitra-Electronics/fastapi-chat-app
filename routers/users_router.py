from fastapi import APIRouter, Depends
from utils import get_current_active_user
from schemas import User
from config import USERS_TAGS, USERS_ME_PREFIX
from routers.users_me_router import me

route = APIRouter(tags=USERS_TAGS)

route.include_router(me, prefix=USERS_ME_PREFIX)

@route.get("/search/")
async def read_own_items(term: str,current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]



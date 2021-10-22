from pydantic.networks import EmailStr, HttpUrl
import pymongo
from datetime import datetime

from config import MONGO_DB_DATABASE, MONGO_DB_URL
from schemas import User, UserInDB, UserUpdate

client = pymongo.MongoClient(MONGO_DB_URL)
db_ = client.get_database(MONGO_DB_DATABASE)
fake_users_db__ = db_.users


def insert__(password: str, full_name: str, email: str, url: HttpUrl, gender: str, recovery: EmailStr) -> None:
    fake_users_db__.insert_one({
        "full_name": full_name,
        "email": email,
        "hashed_password": password,
        "profile_pic_url": url,
        "disabled": False,
        "gender": gender,
        "recovery_email": recovery,
        "joining_date":datetime.utcnow().strftime("%d-%m-%Y"),
        "is_admin": False,
        "is_superuser": False
    })


def update_password(email: EmailStr, password: str) -> None:
    fake_users_db__.update_one({"email": email}, {
                               "$set": {"hashed_password": password}})


def delete(user: User) -> None:
    fake_users_db__.delete_one(
        {"email": user.email, "disabled": user.disabled, "full_name": user.full_name})

def get_user(email: EmailStr) -> UserInDB or None:
    search = list(fake_users_db__.find({"email":email}))
    if search != []:
        user_dict = search[0]
        return UserInDB(**user_dict)


def update_user_in_db__(email: EmailStr, user: UserUpdate) -> bool:
    if not get_user(user.email):
        fake_users_db__.update_one({"email": email}, {
                               "$set": {"full_name": user.full_name, "email": user.email, "profile_pic_url": user.profile_pic_url, "gender": user.gender}})
        return True
    else:
        return False


def search_user_in_db(name: str) -> list:
    return list(fake_users_db__.find({"full_name":{"$regex":name}}))


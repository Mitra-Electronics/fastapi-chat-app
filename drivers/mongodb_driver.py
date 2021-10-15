from pydantic.networks import EmailStr, HttpUrl
import pymongo

from config import MONGO_DB_DATABASE, MONGO_DB_URL
from schemas import User, UserInDB, UserUpdate

client = pymongo.MongoClient(MONGO_DB_URL)
db_ = client.get_database(MONGO_DB_DATABASE)
fake_users_db__ = db_.users


def insert__(username: str, password: str, full_name: str, email: str, url: HttpUrl, gender: str, recovery: EmailStr):
    fake_users_db__.insert_one({
        "username": username,
        "full_name": full_name,
        "email": email,
        "hashed_password": password,
        "profile_pic_url": url,
        "disabled": False,
        "gender": gender,
        "recovery_email": recovery,
        "is_admin": False,
        "is_superuser": False
    })


def update_password(username: str, email: EmailStr, password: str):
    fake_users_db__.update_one({"username": username, "email": email}, {
                               "$set": {"hashed_password": password}})


def delete(user: User):
    fake_users_db__.delete_one(
        {"username": user.username, "email": user.email, "disabled": user.disabled, "full_name": user.full_name})


def update_user_in_db__(username: str, email: EmailStr, user: UserUpdate):
    fake_users_db__.update_one({"username": username, "email": email}, {
                               "$set": {"full_name": user.full_name, "email": user.email, "profile_pic_url": user.profile_pic_url, "gender": user.gender}})


def get_user(username: str, email=None):
    if email is None:
        search = {"username": username}
    else:
        search = {"username": username, "email": email}
    search = list(fake_users_db__.find(search))
    if search != []:
        user_dict = search[0]
        return UserInDB(**user_dict)

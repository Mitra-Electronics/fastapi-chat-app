import pymongo

from config import MONGO_DB_DATABASE, MONGO_DB_URL
from schemas import User

client = pymongo.MongoClient(MONGO_DB_URL)
db_ = client.get_database(MONGO_DB_DATABASE)
fake_users_db__ = db_.users


def insert__(username: str, password: str, full_name: str, email: str):
    fake_users_db__.insert_one({
        "username": username,
        "full_name": full_name,
        "email": email,
        "hashed_password": password,
        "disabled": False,
    })


def update_password(username: str, email: str, password: str):
    fake_users_db__.update_one({"username": username, "email": email}, {
                               "$set": {"hashed_password": password}})


def delete(user: User):
    fake_users_db__.delete_one(
        {"username": user.username, "email": user.email, "disabled": user.disabled, "full_name": user.full_name})

def update_user_in_db(username: str, email: str, password: str):
    fake_users_db__.update_one({"username": username, "email": email, "password":password},{
                               "$set": {"hashed_password": password}})

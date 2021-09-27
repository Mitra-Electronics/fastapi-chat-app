import pymongo

from config import MONGO_DB_DATABASE, MONGO_DB_URL

client = pymongo.MongoClient(MONGO_DB_URL)
db_ = client.get_database(MONGO_DB_DATABASE)
fake_users_db__ = db_.users

def insert(username: str, password: str, full_name: str, email: str):
    fake_users_db__.insert_one({
            "username": username,
            "full_name": full_name,
            "email": email,
            "hashed_password": password,
            "disabled": False,
        })
        
def update_password(username: str, email: str, password: str):
    fake_users_db__.update_one({"username": username, "email": email}, {"$set": {"hashed_password": password}})
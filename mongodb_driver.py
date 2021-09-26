import pymongo

from config import MONGO_DB_DATABASE, MONGO_DB_URL

client = pymongo.MongoClient(MONGO_DB_URL)
db_ = client.get_database(MONGO_DB_DATABASE)
fake_users_db__ = db_.users

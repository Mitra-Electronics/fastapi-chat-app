import secrets
from pydantic.networks import EmailStr
from datetime import datetime
from fastapi.exceptions import HTTPException
from starlette import status 

from drivers.mongodb_driver import db_, get_user

token_db = db_.token

def generate_token():
    tokn =  secrets.token_urlsafe(150)
    if list(token_db.find({"token":tokn})) == []:
        generate_token()
    return tokn

def create_token(email: EmailStr):
    if list(token_db.find({"email":email})) == []:
        raise HTTPException(status_code=403,detail="Token already send")
    else:
        if get_user(email):
            tokn = generate_token()
            token_db.insert_one({"email":email,
                            "token":tokn,
                            "time":datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")})
        else:
            raise HTTPException(status_code=404, detail="User doesn't exists")



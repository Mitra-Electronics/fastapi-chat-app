import secrets
from pydantic.networks import EmailStr
from datetime import datetime
from fastapi.exceptions import HTTPException
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
from fastapi import status

from drivers.mongodb_driver import db_, get_user, update_disabled

conf = ConnectionConfig(
    MAIL_USERNAME = "backup.ishanfiles@gmail.com",
    MAIL_PASSWORD = "jsvhvblwovuzsapt",
    MAIL_FROM = "ishanmitra020@gmail.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_FROM_NAME="Chat app",
    MAIL_TLS = True,
    MAIL_SSL = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True,
    TEMPLATE_FOLDER='./templates'
)

token_db = db_.token

def generate_token():
    tokn =  secrets.token_urlsafe(6)
    if list(token_db.find({"token":tokn})) != []:
        generate_token()
    return tokn

async def create_token(email: EmailStr):
    if list(token_db.find({"email":email})) != []:
        raise HTTPException(status_code=403,detail="Token already send")
    else:
        if get_user(email):
            toknf = generate_token()
            token_db.insert_one({"email":email,
                            "token":toknf,
                            "time":datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")})
            
            fm = FastMail(conf)
            message = MessageSchema(
                subject="Fastapi-Mail module",
                recipients=[email],  # List of recipients, as many as you can pass 
                subtype="html",
                template_body={"otp":str(toknf)},
                )
            await fm.send_message(message, template_name="email_template.html")

        else:
            raise HTTPException(status_code=404, detail="User doesn't exists")

def verify(token: str):
    buffer =list(token_db.find({"token":token}))
    if buffer != []:
        update_disabled(buffer[0]["email"])
    else:
        print(buffer)
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Token does not exist")
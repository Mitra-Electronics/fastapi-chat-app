from datetime import timedelta

from fastapi import HTTPException

NAME = "User authentication testing"
DESCRIPTION = "<h1>Interactive Swagger documentation for testing this api</h1>"
SECRET_KEY = "b9ae2698ad9ba101e6d91f57bb883ec2723fa88a183c72d24f7b9f783c43a56476ab71abfb7905eaf543fc0290cbe30ecb5d002ced2aa94aadb702921f403ee4"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = timedelta(minutes=60 * 12)
MONGO_DB_URL = "mongodb+srv://main:Esa?XD6GyTCY7ktQ@iot.me4b4.mongodb.net/iot_proj?retryWrites=true&w=majority"
MONGO_DB_DATABASE = "iot"
DOCS_URL = "/docs"
REDOC_URL = "/redoc"
OPENAPI_URL = "/openapi.json"
PEPPER = "954076b3cf008298642f0ed45e902bea3c798d5b6308a48af52f5"
TOKEN_URL = "login"
TOKEN_TEST_URL = "test/login"
SCHEMES = ["bcrypt"]
DEPRECATED = "auto"
LOGIN_FORM_TITLE = "Login form"
USER_DISABLED_TEXT = "Disabled"
OAUTH2_REDIRRECT_URL = "/docs/oauth2-redirect"
CREDENTIALS_EXCEPTION = HTTPException(
    status_code=401,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)
INACTIVE_EXCEPTION = HTTPException(status_code=400, detail="Inactive user")

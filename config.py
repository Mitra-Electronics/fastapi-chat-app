from datetime import timedelta

from fastapi import HTTPException

# Fastapi Config
NAME = "User authentication testing"
DESCRIPTION = "<h1>Interactive Swagger documentation for testing this api</h1>"
DOCS_URL = "docs"
REDOC_URL = "redoc"
OPENAPI_URL = "/openapi.json"
OAUTH2_REDIRRECT_URL = "/docs/oauth2-redirect"
LOGIN_FORM_TITLE = "Login form"

# CryptContext Config
SECRET_KEY = "b9ae2698ad9ba101e6d91f57bb883ec2723fa88a183c72d24f7b9f783c43a56476ab71abfb7905eaf543fc0290cbe30ecb5d002ced2aa94aadb702921f403ee4"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = timedelta(minutes=60 * 12)
PEPPER = "954076b3cf008298642f0ed45e902bea3c798d5b6308a48af52f5"
SCHEMES = ["bcrypt"]
DEPRECATED = "auto"

# MongoDb Config
MONGO_DB_URL = "mongodb+srv://main:main@cluster0.me4b4.mongodb.net/myFirstDatabase?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE"
#MONGO_DB_URL = "mongodb://localhost:27017"
#MONGO_DB_URL = "mongodb+srv://main:Esa?XD6GyTCY7ktQ@iot.me4b4.mongodb.net/iot_proj?retryWrites=true&w=majority"
MONGO_DB_DATABASE = "iot"

# Cloudinary Config
CLOUDINARY_CLOUD_NAME = "dyq1mevvs"
CLOUDINARY_CLOUD_API_KEY = "667459361613199"
CLOUDINARY_CLOUD_API_SECRET = "6KGsJIlQbcGwU_irAEviB8fzYeQ"

# CORSMiddleware Config
ORIGINS = [
    "http://localhost:3000",
]
METHODS = ["GET", "POST"]
HEADERS = ["*"]
ALLOW_CREDENTIALS = True

# Users Router Config
USERS_TAGS = ["Users"]
USERS_ME_TAGS = ["Me"]
USERS_PREFIX = "/users"
USERS_ME_PREFIX = "/me"

# Url Config
TOKEN_URL = "login"
TOKEN_TEST_URL = "test/login"

# Static Config
STATIC_URL = "/static"
STATIC_DIR = "static"
STATIC_NAME = "static"

# Text Config
USER_DISABLED_TEXT = "Disabled"
EMAIL_EXISTS_TEXT = "Email exists"

# Exceptions Config
CREDENTIALS_EXCEPTION = HTTPException(
    status_code=401,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)
INACTIVE_EXCEPTION = HTTPException(status_code=400, detail="Inactive user")

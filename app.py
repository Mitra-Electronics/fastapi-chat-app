from fastapi import Depends, FastAPI, HTTPException, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.param_functions import File
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm

from drivers.cloudinary_driver import upload_pic
from config import (ACCESS_TOKEN_EXPIRE_MINUTES, ALLOW_CREDENTIALS,
                    DESCRIPTION, DOCS_URL, HEADERS, METHODS, NAME,
                    OAUTH2_REDIRRECT_URL, OPENAPI_URL, ORIGINS, REDOC_URL,
                    STATIC_DIR, STATIC_NAME, STATIC_URL, TOKEN_TEST_URL,
                    TOKEN_URL, USER_DISABLED_TEXT, USERS_PREFIX)
from schemas import Token, UserLogin, UserSignup
from routers.users_router import route
from utils import (authenticate_user, create_access_token,
                   register_user)

app = FastAPI(docs_url="/"+DOCS_URL, redoc_url="/"+REDOC_URL, openapi_url=OPENAPI_URL,
              swagger_ui_oauth2_redirect_url=OAUTH2_REDIRRECT_URL, title=NAME, description=DESCRIPTION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=ALLOW_CREDENTIALS,
    allow_methods=METHODS,
    allow_headers=HEADERS,
)

app.include_router(route, prefix=USERS_PREFIX)
# to get a string like this run:
# openssl rand -hex 32


@app.post("/"+TOKEN_TEST_URL, response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login"""
    user = authenticate_user(
        form_data.username, form_data.password)
    if not user:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},

        )
    if user == USER_DISABLED_TEXT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is disabled",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(

        data={"sub": user.email}, expires_delta=ACCESS_TOKEN_EXPIRE_MINUTES

    )

    return JSONResponse({"access_token": access_token, "token_type": "bearer"})


@app.post("/"+TOKEN_URL, response_model=Token)
async def login_for_access_token(form_data: UserLogin):
    """Login"""
    user = authenticate_user(
        form_data.email, form_data.password)
    if not user:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},

        )
    if user == USER_DISABLED_TEXT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is disabled",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token({"sub": user.email}, ACCESS_TOKEN_EXPIRE_MINUTES)

    return JSONResponse({"access_token": access_token, "token_type": "bearer"})


@app.post("/register", response_model=Token)
async def register_user_(user: UserSignup):
    user_create = register_user(
        user, user.profile_pic_url, user.gender)
    if user_create is True:
        user = authenticate_user(
            user.email, user.password)
        if not user:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if user == USER_DISABLED_TEXT:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is disabled",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = create_access_token(
            data={"sub": user.email}, expires_delta=ACCESS_TOKEN_EXPIRE_MINUTES
        )

        return JSONResponse({"access_token": access_token, "token_type": "bearer"})
    else:
        raise HTTPException(
            status_code=status.HTTP_226_IM_USED,
            detail="User already exists",
            headers={"WWW-Authenticate": "Bearer"},
        )


@app.get("/file", response_class=RedirectResponse)
async def file_send():
    return RedirectResponse("http://res.cloudinary.com/dyq1mevvs/image/upload/v1633674919/q5mexicgwoyj8xjduxca.jpg")


@app.post("/upload")
async def upload_picture_to_cloudinary_(pic: UploadFile = File(...)):
    return upload_pic(pic)


@app.get('/')
async def redirrect():
    return RedirectResponse("/"+DOCS_URL)

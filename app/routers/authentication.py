import hashlib
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
import config.env as env
from database.config import SessionLocal
from sqlalchemy.orm import Session
import utils.crud_account as crud_a
from models.account import AccountCreate as AC


router = APIRouter(
    prefix="/api/auth",
    tags=["authentication"]
)

secret_key = env.SECRET_KEY if env.SECRET_KEY is not None else ""
manager = LoginManager(secret_key, "/api/auth/login/")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def hash_password(password: str, secret_key: str) -> str:
    b_pw = password.encode(encoding="utf-8")
    b_secret_key = secret_key.encode(encoding="utf-8")
    b_hashed_pw = hashlib.pbkdf2_hmac("sha256", b_pw, b_secret_key, 1000)
    return b_hashed_pw.hex()


@router.post("/register/")
async def register_account(
        register_item: AC,
        db: Session = Depends(get_db)):
    """アカウント作成API

    Args:
        register_item (AC): アカウント情報(IDとPW).

    Raises:
        HTTPException: HTTP_400_BAD_REQUEST
        HTTPException: HTTP_500_INTERNAL_SERVER_ERROR

    Returns:
        Response: HTTP_201_CREATED
    """
    secret_key = env.SECRET_KEY

    if secret_key is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if crud_a.count_list_by_name(db, register_item.name) > 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    register_item.password = hash_password(register_item.password, secret_key)

    res = crud_a.create_account(db, register_item)
    if res is not None:
        return JSONResponse(status_code=status.HTTP_201_CREATED)
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@manager.user_loader
def get_user_by_name(name: str, db: Session = None):
    res = None
    if db is None:
        db = SessionLocal()
        try:
            res = crud_a.get_user_by_name(db, name)
        finally:
            db.close()
    else:
        res = crud_a.get_user_by_name(db, name)
    return res


@router.post("/login/")
async def login(
        data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)):
    """ログイン用API

    Args:
        data (OAuth2PasswordRequestForm, optional): IDとPW. Defaults to Depends().

    Raises:
        InvalidCredentialsException: トークンが存在しない場合に発生する例外.

    Returns:
        Response: HTTP_200_OK. アクセストークン(access_token).
    """
    name = data.username
    password = data.password
    hashed_pw = hash_password(password, secret_key)

    user = crud_a.get_user_by_name(db, name)

    if user is None:
        raise InvalidCredentialsException
    elif user.password != hashed_pw:
        raise InvalidCredentialsException

    access_token = manager.create_access_token(
        data={"sub": name}
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK, content={
            "access_token": access_token,
            "token_type": "Bearer"})

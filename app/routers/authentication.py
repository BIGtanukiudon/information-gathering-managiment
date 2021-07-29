import hashlib
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
import config.env as env
from database.config import SessionLocal
from sqlalchemy.orm import Session
import utils.crud_account as crud_a
from models.account import AccountCreate as AC


router = APIRouter(
    prefix="/api/auth",
    tags=["authentication"]
)


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

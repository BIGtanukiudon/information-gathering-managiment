from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from models.collection_destination import CollectionDestination as CD, CollectionDestinationCreate as CDC
from database.config import SessionLocal
from sqlalchemy.orm import Session
import utils.crud_collection_destination as crud_cd
from routers.authentication import manager


router = APIRouter(
    prefix="/api/collection_destination",
    tags=["collection_destination"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/{collection_destination_id}", response_model=CD)
async def get_collection_destination(
        db: Session = Depends(get_db),
        collection_destination_id: int = 0):
    """収集先情報取得API

    Args:
        collection_destination_id (int, optional): 収集先ID. Defaults to 0.

    Raises:
        HTTPException: HTTP_400_BAD_REQUEST
        HTTPException: TTP_404_NOT_FOUND

    Returns:
        Response: HTTP_200_OK
    """
    if collection_destination_id <= 0:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST)

    res = crud_cd.get_collection_destination(db, collection_destination_id)
    if res is not None:
        return res
    else:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)


@router.get("/list/", response_model=List[CD])
async def get_collection_destination_list(db: Session = Depends(get_db)):
    """収集先情報リスト取得API

    Raises:
        HTTPException: HTTP_404_NOT_FOUND

    Returns:
        Response: HTTP_200_OK
    """
    res = crud_cd.get_collection_destination_list(db)
    if len(res) == 0:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)
    elif len(res) > 0:
        return res


@router.post("/register/")
async def register_collection_destination(
        register_item: CDC,
        db: Session = Depends(get_db),
        user=Depends(manager)):
    """収集先情報登録API

    Args:
        register_item (CDC): 収集先情報.

    Raises:
        HTTPException: HTTP_500_INTERNAL_SERVER_ERROR

    Returns:
        Response: HTTP_201_CREATED

    Note:
        登録する収集先情報について。

        name: 収集先の名前。
        domain: 収集先のドメイン。
        contents_attr_name: 記事部分だと判断できるclass属性のクラス名等。（例：.entry-content。ドットまで入れる。）
        title_attr_name: 記事タイトル部分だと判断できるclass属性のクラス名やname属性の値等。（例：.title。ドットまで入れる。）
        published_date_attr_name: 公開日部分だと判断できるclass属性のクラス名やname属性の値等。（例：.published-at。ドットまで入れる。）
        content_url_attr_name: 記事本文へ遷移するURL部分だと判断できるclass属性のクラス名やname属性の値等。（例：.content-url。ドットまで入れる。）
        account_id: アカウントID。基本は0でOK。
    """
    user_id = user.id
    register_item.account_id = user_id

    res = crud_cd.create_collection_destination(db, register_item)
    if res is not None:
        return JSONResponse(status_code=status.HTTP_201_CREATED)
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete("/{collection_destination_id}", response_model=CD)
async def delete_collection_destination(
        db: Session = Depends(get_db),
        collection_destination_id: int = 0,
        user=Depends(manager)):
    """収集先情報削除API

    Args:
        collection_destination_id (int, optional): 収集先ID. Defaults to 0.

    Raises:
        HTTPException: HTTP_400_BAD_REQUEST
        HTTPException: TTP_404_NOT_FOUND
        HTTPException: HTTP_500_INTERNAL_SERVER_ERROR

    Returns:
        Response: HTTP_204_NO_CONTENT
    """
    if collection_destination_id <= 0:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST)

    res = crud_cd.delete_collection_destination(db, collection_destination_id)
    if res == 204:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    elif res is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)
    elif res == 500:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR)

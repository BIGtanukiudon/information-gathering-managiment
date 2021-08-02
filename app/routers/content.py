from datetime import date, datetime
from typing import List
from utils.scraping import scraping_contents as sc
import utils.crud_collection_destination as crud_cd
import utils.crud_content as crud_c
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from models.collection_destination import CollectionDestinationCreate as CDC
from models.content import Content as MC, ContentCreate as CC
from models.scraping import ScrapingContent as SCM
from database.config import SessionLocal
from sqlalchemy.orm import Session
from routers.authentication import manager

router = APIRouter(
    prefix="/api/content",
    tags=["content"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/list/{limit}", response_model=List[MC])
async def get_content_list(db: Session = Depends(get_db), limit: int = 30):
    res = crud_c.get_content_list(db, limit)
    if len(res) == 0:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)
    elif len(res) > 0:
        return res


@router.post("/scraping_contents/", response_model=List[CC])
async def scraping_contents(
        db: Session = Depends(get_db),
        user=Depends(manager)):
    collection_destination_list = crud_cd.get_collection_destination_list(db)

    if len(collection_destination_list) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    registered_content_list = crud_c.get_content_list(db, 0)

    create_content_list: List[CC] = []
    for collection_destination in collection_destination_list:
        cd_id = collection_destination.id
        account_id = user.id

        scraping_contents: List[SCM] = sc(
            collection_destination.domain,
            collection_destination.contents_attr_name,
            collection_destination.title_attr_name,
            collection_destination.published_date_attr_name,
            collection_destination.content_url_attr_name)

        for scraping_content in scraping_contents:
            today = date.today()
            is_registerd = next(
                filter(
                    lambda x: x.title == scraping_content.title,
                    registered_content_list), None) is not None

            # 当日の日付のもの及び、まだ登録が無いものを登録
            if today == datetime.date(
                    scraping_content.published_at) and is_registerd is False:
                content = CC(
                    title=scraping_content.title,
                    content_url=scraping_content.content_url,
                    published_at=scraping_content.published_at,
                    domain=scraping_content.domain,
                    is_read_later=False,
                    collection_destination_id=cd_id,
                    account_id=account_id
                )
                create_content_list.append(content)

    if len(create_content_list) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    res = crud_c.create_content_list(db, create_content_list)
    if res:
        return create_content_list
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post("/test_scraping_contents/")
async def test_scraping_contents(
        collection_destination: CDC,
        user=Depends(manager)):
    scraping_contents: List[SCM] = sc(
        collection_destination.domain,
        collection_destination.contents_attr_name,
        collection_destination.title_attr_name,
        collection_destination.published_date_attr_name,
        collection_destination.content_url_attr_name)
    if len(scraping_contents) > 0:
        return scraping_contents
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

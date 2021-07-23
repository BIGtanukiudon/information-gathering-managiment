from datetime import datetime
from typing import List
from utils.scraping import scraping_contents as sc
import utils.crud_collection_destination as crud_cd
import utils.crud_content as crud_c
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from models.content import ContentCreate as CC
from models.scraping import ScrapingContent as SCM
from database.config import SessionLocal
from sqlalchemy.orm import Session

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


@router.post("/scraping_contents/", response_model=List[CC])
async def scraping_contents(db: Session = Depends(get_db)):
    collection_destination_list = crud_cd.get_collection_destination_list(db)

    if len(collection_destination_list) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    create_content_list: List[CC] = []
    for collection_destination in collection_destination_list:
        cd_id = collection_destination.id
        account_id = collection_destination.account_id

        scraping_contents: List[SCM] = sc(
            collection_destination.domain,
            collection_destination.contents_attr_name,
            collection_destination.title_attr_name,
            collection_destination.published_date_attr_name,
            collection_destination.content_url_attr_name)

        for scraping_content in scraping_contents:
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

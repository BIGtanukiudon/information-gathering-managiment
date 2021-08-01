from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
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
    if collection_destination_id <= 0:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST)

    res = crud_cd.get_collection_destination(db, collection_destination_id)
    if res is not None:
        return res
    else:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)


@router.get("/list/", response_model=List[CD])
async def get_collection_destination_list(db: Session = Depends(get_db)):
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
    user_id = user.id
    register_item.account_id = user_id

    res = crud_cd.create_collection_destination(db, register_item)
    if res is not None:
        return JSONResponse(status_code=status.HTTP_201_CREATED)
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

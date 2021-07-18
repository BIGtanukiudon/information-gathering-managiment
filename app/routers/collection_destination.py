from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from collection_destination import CollectionDestination, CollectionDestinationCreate
from database.models import CollectionDestination as CDDM
from database.config import SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError


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


@router.get("/list")
async def get_list():
    return {"message": "collection_destination list."}


@router.post("/register")
async def register_collection_destination(
        register_item: CollectionDestinationCreate,
        db: Session = Depends(get_db)):
    insert_item = CDDM(**register_item.dict())
    if insert_item is None:
        return JSONResponse(status.HTTP_400_BAD_REQUEST)
    try:
        db.add(insert_item)
        db.commit()
        db.refresh(insert_item)
        return JSONResponse(status_code=status.HTTP_201_CREATED)
    except SQLAlchemyError as e:
        print(e)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

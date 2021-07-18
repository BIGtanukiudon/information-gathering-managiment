from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from collection_destination import CollectionDestinationCreate
from database.models import CollectionDestinationForGet as CDDM4G, CollectionDestinationForCreate as CDDM4C
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


@router.get("/{collection_destination_id}")
async def get_collection_destination(
        db: Session = Depends(get_db),
        collection_destination_id: int = 0):
    if collection_destination_id <= 0:
        return JSONResponse(status_code=HTTP_400_BAD_REQUEST)

    res = db.query(CDDM4G).filter(
        CDDM4G.id == collection_destination_id).first()
    if res is not None:
        return res
    else:
        return HTTP_404_NOT_FOUND


@router.get("/list")
async def get_collection_destination_list(db: Session = Depends(get_db)):
    res = db.query(CDDM4G).order_by(CDDM4G.updated_at).all()
    if len(res) == 0:
        return HTTP_404_NOT_FOUND
    elif len(res) > 0:
        return res


@router.post("/register")
async def register_collection_destination(
        register_item: CollectionDestinationCreate,
        db: Session = Depends(get_db)):
    insert_item = CDDM4C(**register_item.dict())
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

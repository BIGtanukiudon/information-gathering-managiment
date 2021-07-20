from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from database.models import CollectionDestinationForGet as CDDM4G, CollectionDestinationForCreate as CDDM4C
from models.collection_destination import CollectionDestinationCreate as CDC


def get_collection_destination(db: Session, collection_destination_id: int):
    return db.query(CDDM4G).filter(
        CDDM4G.id == collection_destination_id).first()


def get_collection_destination_list(db: Session):
    return db.query(CDDM4G).order_by(CDDM4G.updated_at).all()


def create_collection_destination(db: Session, item: CDC):
    db_item = CDDM4C(**item.dict())
    try:
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    except SQLAlchemyError as e:
        print(e)
        return None

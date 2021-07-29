from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from database.models import AccountForGet as AM4G, AccountForCreate as AM4C
from models.account import AccountCreate as AC


def create_account(db: Session, item: AC):
    db_item = AM4C(**item.dict())
    try:
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    except SQLAlchemyError as e:
        print(e)
        return None


def count_list_by_name(db: Session, name: str) -> int:
    count: int = 0
    if name != "":
        count = db.query(AM4G).filter(AM4G.name == name).count()
    return count

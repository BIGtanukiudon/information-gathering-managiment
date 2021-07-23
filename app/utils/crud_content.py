from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from database.models import ContentForCreate as C4C
from models.content import ContentCreate as CC


def create_content_list(db: Session, item_list: List[CC]):
    try:
        for item in item_list:
            db_item = C4C(**item.dict())
            # 以下の処理はパフォーマンス最悪なので、改善する
            db.add(db_item)
        db.commit()
        return True
    except SQLAlchemyError as e:
        print(e)
        return False

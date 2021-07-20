from datetime import datetime
from pydantic import BaseModel


class CollectionDestinationBase(BaseModel):
    name: str
    domain: str
    contents_attr_name: str
    title_attr_name: str
    published_date_attr_name: str
    content_url_attr_name: str
    account_id: int


class CollectionDestination(CollectionDestinationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class CollectionDestinationCreate(CollectionDestinationBase):
    name: str
    domain: str
    contents_attr_name: str
    title_attr_name: str
    published_date_attr_name: str
    content_url_attr_name: str
    account_id: int

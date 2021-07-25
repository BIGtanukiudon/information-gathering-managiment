from datetime import datetime
from pydantic import BaseModel


class ContentBase(BaseModel):
    title: str
    content_url: str
    published_at: datetime
    domain: str


class Content(ContentBase):
    id: int
    collection_destination_id: int
    account_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class ContentCreate(ContentBase):
    is_read_later: bool
    collection_destination_id: int
    account_id: int

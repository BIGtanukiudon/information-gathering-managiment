from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ContentBase(BaseModel):
    id: Optional[int]
    title: Optional[str]
    content_url: Optional[str]
    published_at: Optional[datetime]
    domain: Optional[str]
    is_read_later: Optional[bool]
    collection_destination_id: Optional[int]
    user_id: Optional[int]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class ContentCreate(ContentBase):
    title: str
    content_url: str
    published_at: datetime
    domain: str
    is_read_later: bool
    collection_destination_id: int
    user_id: int

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class CollectionDestinationBase(BaseModel):
    id: Optional[int]
    name: Optional[str]
    domai: Optional[str]
    contents_class_name: Optional[str]
    title_class_name: Optional[str]
    published_date_class_name: Optional[str]
    is_getting_domain: Optional[bool]
    content_url_class_name: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class CollectionDestinationCreate(CollectionDestinationBase):
    name: str
    domai: str
    contents_class_name: str
    title_class_name: str
    published_date_class_name: str
    is_getting_domain: bool
    content_url_class_name: str

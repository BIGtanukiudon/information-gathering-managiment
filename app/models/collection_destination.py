from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class CollectionDestinationBase(BaseModel):
    id: Optional[int]
    name: Optional[str]
    domai: Optional[str]
    contents_attr_name: Optional[str]
    title_attr_name: Optional[str]
    published_date_attr_name: Optional[str]
    is_getting_domain: Optional[bool]
    domain_attr_name: Optional[str]
    content_url_attr_name: Optional[str]
    user_id: Optional[int]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class CollectionDestinationCreate(CollectionDestinationBase):
    name: str
    domai: str
    contents_attr_name: str
    title_attr_name: str
    published_date_attr_name: str
    is_getting_domain: bool
    domain_attr_name: str
    content_url_attr_name: str
    user_id: int

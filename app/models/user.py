from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    id: Optional[int]
    name: Optional[str]
    password: Optional[str]
    is_active: Optional[bool]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class UserCreate(UserBase):
    name: str
    password: str

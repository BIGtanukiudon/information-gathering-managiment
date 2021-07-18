from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class AccountBase(BaseModel):
    id: Optional[int]
    name: Optional[str]
    password: Optional[str]
    is_active: Optional[bool]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class AccountCreate(AccountBase):
    name: str
    password: str

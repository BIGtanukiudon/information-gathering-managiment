from datetime import datetime
from pydantic import BaseModel


class AccountBase(BaseModel):
    name: str
    password: str


class Account(BaseModel):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime


class AccountCreate(AccountBase):
    pass

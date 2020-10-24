from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class BaseUser(BaseModel):
    identity_card: str
    names: str
    surnames: str
    phone: str
    email: str


class CreateUser(BaseUser):
    pass


class PayloadUser(BaseModel):
    identity_card: Optional[str]
    names: Optional[str]
    surnames: Optional[str]
    phone: Optional[str]
    email: Optional[str]


class UpdateUser(BaseModel):
    names: Optional[str]
    surnames: Optional[str]
    phone: Optional[str]
    email: Optional[str]


class UserInDB(BaseUser):
    # id: int
    created_at: datetime
    last_modified: datetime


class User(UserInDB):
    pass

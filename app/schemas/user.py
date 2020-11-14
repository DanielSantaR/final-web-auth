from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic.networks import EmailStr


class BaseUser(BaseModel):
    identity_card: str
    names: str
    surnames: str
    phone: str
    email: EmailStr


class CreateUser(BaseUser):
    pass


class UpdateUser(BaseModel):
    names: Optional[str]
    surnames: Optional[str]
    phone: Optional[str]
    email: Optional[EmailStr]


class UserInDB(BaseUser):
    created_at: datetime
    last_modified: datetime


class User(UserInDB):
    pass

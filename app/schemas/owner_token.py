from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class BaseOwnerToken(BaseModel):
    code: str
    owner_id: str
    token: str
    token_type: str


class CreateOwnerToken(BaseOwnerToken):
    pass


class UpdateOwnerToken(BaseModel):
    code: Optional[str]
    owner_id: Optional[str]
    token: Optional[str]
    token_type: Optional[str]


class OwnerTokenInDB(BaseOwnerToken):
    created_at: datetime


class OwnerToken(OwnerTokenInDB):
    pass

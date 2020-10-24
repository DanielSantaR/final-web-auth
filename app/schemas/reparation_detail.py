from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class BaseReparationDetail(BaseModel):
    vehicle: str
    employee: str
    description: str
    cost: float
    spare_parts: List
    state: str


class CreateReparationDetail(BaseReparationDetail):
    pass


class PayloadReparationDetail(BaseModel):
    vehicle: Optional[int]
    employee: Optional[str]
    state: Optional[str]


class UpdateReparationDetail(BaseModel):
    vehicle: int
    employee: Optional[str]
    description: Optional[str]
    cost: Optional[float]
    spare_parts: Optional[List]
    state: Optional[str]


class ReparationDetailInDB(BaseReparationDetail):
    # id: int
    created_at: datetime
    last_modified: datetime

    class Config:
        orm_mode = True

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class BaseReparationDetail(BaseModel):
    description: str
    cost: Optional[float]
    spare_parts: Optional[List[str]]
    state: str
    vehicle_id: str
    employee_id: str


class CreateReparationDetail(BaseReparationDetail):
    pass


class UpdateReparationDetail(BaseModel):
    description: Optional[str]
    cost: Optional[float]
    spare_parts: Optional[List[str]]
    state: Optional[str]


class ReparationDetailInDB(BaseReparationDetail):
    id: int
    created_at: datetime
    last_modified: datetime


class ReparationDetail(ReparationDetailInDB):
    pass

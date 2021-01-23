from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class BaseReparationDetail(BaseModel):
    description: str
    cost: Optional[float]
    spare_parts: Optional[List[str]]
    state: str


class CreateReparationDetail(BaseReparationDetail):
    employee_id: str
    vehicle_id: str


class UpdateReparationDetail(BaseModel):
    employee_id: Optional[str]
    description: Optional[str]
    cost: Optional[float]
    spare_parts: Optional[List[str]]
    state: Optional[str]


class ReparationDetailInDB(BaseReparationDetail):
    id: int
    employee_id: str
    vehicle_id: str
    created_at: datetime
    last_modified: datetime


class ReparationDetail(ReparationDetailInDB):
    pass

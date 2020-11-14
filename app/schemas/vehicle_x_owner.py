from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class BaseVehicleXOwner(BaseModel):
    vehicle_id: str
    owner_id: str


class CreateVehicleXOwner(BaseVehicleXOwner):
    pass


class UpdateVehicleXOwner(BaseModel):
    vehicle_id: Optional[str]
    owner_id: Optional[str]


class VehicleXOwnerInDB(BaseVehicleXOwner):
    id: int
    created_at: datetime
    last_modified: datetime


class VehicleXOwner(VehicleXOwnerInDB):
    pass

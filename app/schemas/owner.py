from datetime import datetime
from typing import Optional

from app.schemas.user import BaseUser, UpdateUser, UserInDB


class BaseOwner(BaseUser):
    pass


class CreateOwner(BaseOwner):
    creation_employee_id: str
    update_employee_id: str


class UpdateOwner(UpdateUser):
    update_employee_id: Optional[str]


class OwnerInDB(UserInDB):
    creation_employee_id: str
    update_employee_id: str
    created_at: datetime
    last_modified: datetime


class Owner(OwnerInDB):
    pass

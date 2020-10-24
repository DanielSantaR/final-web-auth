from typing import Optional

from app.schemas.user import BaseUser, PayloadUser, UpdateUser, UserInDB


class BaseOwner(BaseUser):
    pass


class CreateOwner(BaseOwner):
    creation_employee: str
    update_employee: str


class PayloadOwner(PayloadUser):
    creation_employee: Optional[str]
    update_employee: Optional[str]
    vehicle: Optional[int]


class UpdateOwner(UpdateUser):
    update_employee: Optional[str]
    vehicle: Optional[int]


class OwnerInDB(UserInDB):
    pass


class Owner(OwnerInDB):
    pass

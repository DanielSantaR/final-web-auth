from enum import Enum
from typing import Optional

from app.schemas.user import BaseUser, PayloadUser, UpdateUser, UserInDB


class Role(str, Enum):
    manager = "manager"
    assitant = "assitant"
    supervisor = "supervisor"
    technician = "technician"


class BaseEmployee(BaseUser):
    username: str
    is_active: bool = True
    role: Role


class CreateEmployee(BaseEmployee):
    password: str


class PayloadEmployee(PayloadUser):
    username: Optional[str]
    is_active: Optional[bool]
    role: Optional[Role]


class UpdateEmployee(UpdateUser):
    username: Optional[str]
    password: Optional[str]
    is_active: Optional[bool]
    role: Optional[Role]


class EmployeeInDB(UserInDB, BaseEmployee):
    pass


class Employee(EmployeeInDB):
    pass

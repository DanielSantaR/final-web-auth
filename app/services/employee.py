from typing import List

from app.core.config import Settings, get_settings
from app.core.security import get_password_hash
from app.infra.httpx.client import HTTPXClient
from app.schemas.employee import CreateEmployee, Employee, EmployeeInDB, UpdateEmployee
from app.schemas.search import EmployeeQueryParams

httpx_client = HTTPXClient()

settings: Settings = get_settings()


class EmployeeService:
    def __init__(self):
        return

    async def get_by_id(self, *, employee_id: int) -> Employee:
        url = f"{settings.DATABASE_URL}/api/employees/{employee_id}"
        header = {"Content-Type": "application/json"}
        response = await httpx_client.get(
            url_service=url, status_response=200, headers=header, timeout=40
        )
        return response

    async def get_by_username(self, *, username: str) -> Employee:
        url = f"{settings.DATABASE_URL}/api/employees/username/{username}"
        header = {"Content-Type": "application/json"}
        response = await httpx_client.get(
            url_service=url, status_response=200, headers=header, timeout=40
        )
        return response

    async def create(self, *, employee_in: CreateEmployee) -> CreateEmployee:
        employee_in.password = get_password_hash(employee_in.password)
        url = f"{settings.DATABASE_URL}/api/employees"
        header = {"Content-Type": "application/json"}
        user = employee_in.dict()
        response = await httpx_client.post(
            url_service=url, status_response=201, body=user, headers=header, timeout=40
        )
        return response

    async def update(
        self, *, employee_id: str, employee_in: UpdateEmployee
    ) -> EmployeeInDB:
        url = f"{settings.DATABASE_URL}/api/employees/{employee_id}"
        header = {"Content-Type": "application/json"}
        user = employee_in.dict()
        response = await httpx_client.patch(
            url_service=url, status_response=200, body=user, headers=header, timeout=40
        )
        return response

    async def get_all(
        self, *, query_args: EmployeeQueryParams, skip: int, limit: int
    ) -> List[Employee]:
        url = f"{settings.DATABASE_URL}/api/employees"
        header = {"Content-Type": "application/json"}
        payload = query_args.__dict__
        params = {
            key: value for (key, value) in payload.items() if value not in [None, ""]
        }
        response = await httpx_client.get(
            url_service=url,
            status_response=200,
            params=params,
            headers=header,
            timeout=40,
        )
        return response


employee_service = EmployeeService()

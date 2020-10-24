from app import schemas
from app.core.config import Settings, get_settings
from app.core.security import get_password_hash
from app.infra.httpx.client import HTTPXClient

httpx_client = HTTPXClient()

settings: Settings = get_settings()


async def get_employee_by_id(*, employee_id: int) -> schemas.Employee:
    url = f"{settings.DATABASE_URL}/api/employee/employee-id/{employee_id}/"
    header = {"Content-Type": "application/json"}
    response = await httpx_client.get(
        url_service=url, status_response=200, headers=header, timeout=40
    )
    return response


async def get_employee_by_username(*, username: str) -> schemas.Employee:
    url = f"{settings.DATABASE_URL}/api/employee/username/{username}/"
    header = {"Content-Type": "application/json"}
    response = await httpx_client.get(
        url_service=url, status_response=200, headers=header, timeout=40
    )
    return response


async def create_employee(
    *, employee_in: schemas.CreateEmployee
) -> schemas.CreateEmployee:
    employee_in.password = get_password_hash(employee_in.password)
    url = f"{settings.DATABASE_URL}/api/employee/"
    header = {"Content-Type": "application/json"}
    user = employee_in.dict()
    response = await httpx_client.post(
        url_service=url, status_response=201, body=user, headers=header, timeout=40
    )
    return response

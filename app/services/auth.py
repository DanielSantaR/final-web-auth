from typing import Optional

from app.core.config import Settings, get_settings
from app.core.security import verify_password
from app.infra.httpx.client import HTTPXClient
from app.schemas import Employee

httpx_client = HTTPXClient()

settings: Settings = get_settings()


async def authenticate(*, username: str, password: str) -> Optional[Employee]:
    url = f"{settings.DATABASE_URL}/api/employee/auth/{username}/"
    header = {"Content-Type": "application/json"}
    user = await httpx_client.get(
        url_service=url, status_response=200, headers=header, timeout=40
    )

    if not user:
        return None
    if not verify_password(password, user["password"]):
        return None
    user = Employee(**user)
    return user

from typing import Optional

from app.core.config import Settings, get_settings
from app.core.security import verify_password
from app.infra.httpx.client import HTTPXClient
from app.schemas.employee import Employee
from app.schemas.owner import Owner

httpx_client = HTTPXClient()

settings: Settings = get_settings()


class AuthService:
    def __init__(self):
        return

    async def authenticate(self, *, username: str, password: str) -> Optional[Employee]:
        url = f"{settings.DATABASE_URL}/api/employees/auth/{username}"
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

    async def owner_authenticate(self, *, identity_card: str) -> Optional[Owner]:
        url = f"{settings.DATABASE_URL}/api/owners/{identity_card}"
        header = {"Content-Type": "application/json"}
        user = await httpx_client.get(
            url_service=url, status_response=200, headers=header, timeout=40
        )

        if not user:
            return None
        user = Owner(**user)
        return user


auth_service = AuthService()

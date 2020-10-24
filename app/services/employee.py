from app.core.config import Settings, get_settings
from app.infra.httpx.client import HTTPXClient
from app.schemas import User

httpx_client = HTTPXClient()

settings: Settings = get_settings()


async def get_user_by_id(user_id: int) -> User:
    url = f"{settings.DATABASE_URL}/api/user/user-id/{user_id}/"
    header = {"Content-Type": "application/json"}
    response = await httpx_client.get(
        url_service=url, status_response=200, headers=header, timeout=40
    )
    return response

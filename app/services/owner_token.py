from typing import List

from app.core.config import Settings, get_settings
from app.infra.httpx.client import HTTPXClient
from app.schemas.owner_token import CreateOwnerToken, OwnerToken
from app.schemas.search import OwnerTokenQueryParams

httpx_client = HTTPXClient()

settings: Settings = get_settings()


class OwnerTokenService:
    def __init__(self):
        return

    async def get_by_code(self, *, owner_token_id: str) -> OwnerToken:
        url = f"{settings.DATABASE_URL}/api/owner-tokens/{owner_token_id}"
        header = {"Content-Type": "application/json"}
        response = await httpx_client.get(
            url_service=url, status_response=200, headers=header, timeout=40
        )
        return response

    async def create(self, *, owner_token_in: CreateOwnerToken) -> CreateOwnerToken:
        url = f"{settings.DATABASE_URL}/api/owner-tokens"
        header = {"Content-Type": "application/json"}
        owner_token = owner_token_in.dict()
        response = await httpx_client.post(
            url_service=url,
            status_response=201,
            body=owner_token,
            headers=header,
            timeout=40,
        )
        return response

    async def get_all(
        self,
        *,
        query_args: OwnerTokenQueryParams,
    ) -> List[OwnerToken]:
        url = f"{settings.DATABASE_URL}/api/owner-tokens"
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

    async def delete(self, *, owner_token_id: str) -> OwnerToken:
        url = f"{settings.DATABASE_URL}/api/owner-tokens/{owner_token_id}"
        header = {"Content-Type": "application/json"}
        response = await httpx_client.delete(
            url_service=url, status_response=204, headers=header, timeout=40
        )
        return response


owner_token_service = OwnerTokenService()

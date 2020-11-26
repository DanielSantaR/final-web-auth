from typing import List

from app.core.config import Settings, get_settings
from app.infra.httpx.client import HTTPXClient
from app.schemas.owner import CreateOwner, Owner, OwnerInDB, UpdateOwner
from app.schemas.search import OwnerQueryParams
from app.schemas.vehicle import Vehicle

httpx_client = HTTPXClient()

settings: Settings = get_settings()


class OwnerService:
    def __init__(self):
        return

    async def get_by_id(self, *, owner_id: str) -> Owner:
        url = f"{settings.DATABASE_URL}/api/owners/{owner_id}"
        header = {"Content-Type": "application/json"}
        response = await httpx_client.get(
            url_service=url, status_response=200, headers=header, timeout=40
        )
        return response

    async def get_owner_vehicles(self, *, owner_id: str) -> List[Vehicle]:
        url = f"{settings.DATABASE_URL}/api/vehicles-x-owners/owner/{owner_id}/vehicles"
        header = {"Content-Type": "application/json"}
        response = await httpx_client.get(
            url_service=url, status_response=200, headers=header, timeout=40
        )
        return response

    async def create(self, *, owner_in: CreateOwner) -> CreateOwner:
        url = f"{settings.DATABASE_URL}/api/owners"
        header = {"Content-Type": "application/json"}
        owner = owner_in.dict()
        response = await httpx_client.post(
            url_service=url,
            status_response=201,
            body=owner,
            headers=header,
            timeout=40,
        )
        return response

    async def get_all(
        self,
        *,
        query_args: OwnerQueryParams,
    ) -> List[Owner]:
        url = f"{settings.DATABASE_URL}/api/owners"
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

    async def update(self, *, owner_id: str, owner_in: UpdateOwner) -> OwnerInDB:
        url = f"{settings.DATABASE_URL}/api/owners/{owner_id}"
        header = {"Content-Type": "application/json"}
        user = owner_in.dict()
        response = await httpx_client.patch(
            url_service=url, status_response=200, body=user, headers=header, timeout=40
        )
        return response

    async def delete(self, *, owner_id: str, vehicle_id: str) -> int:
        url = f"{settings.DATABASE_URL}/api/vehicles-x-owners/vehicle/{vehicle_id}/owner/{owner_id}"
        header = {"Content-Type": "application/json"}
        response = await httpx_client.delete(
            url_service=url, status_response=204, headers=header, timeout=40
        )
        return response


owner_service = OwnerService()

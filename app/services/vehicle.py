from typing import List, Optional

from app.core.config import Settings, get_settings
from app.infra.httpx.client import HTTPXClient
from app.schemas.owner import Owner
from app.schemas.search import VehicleQueryParams
from app.schemas.vehicle import CreateVehicle, UpdateVehicle, Vehicle, VehicleInDB
from app.schemas.vehicle_x_owner import VehicleXOwner

httpx_client = HTTPXClient()

settings: Settings = get_settings()


class VehicleService:
    def __init__(self):
        return

    async def get_by_plate(self, *, vehicle_id: str) -> Vehicle:
        url = f"{settings.DATABASE_URL}/api/vehicles/{vehicle_id}"
        header = {"Content-Type": "application/json"}
        response = await httpx_client.get(
            url_service=url, status_response=200, headers=header, timeout=40
        )
        return response

    async def create(self, *, vehicle_in: CreateVehicle) -> CreateVehicle:
        url = f"{settings.DATABASE_URL}/api/vehicles"
        header = {"Content-Type": "application/json"}
        vehicle = vehicle_in.dict()
        response = await httpx_client.post(
            url_service=url,
            status_response=201,
            body=vehicle,
            headers=header,
            timeout=40,
        )
        return response

    async def create_owner_vehicle(
        self, *, vehicle_id: str, owner_id: str
    ) -> VehicleXOwner:
        url = f"{settings.DATABASE_URL}/api/vehicles-x-owners"
        header = {"Content-Type": "application/json"}
        owner_vehicle = {"vehicle_id": vehicle_id, "owner_id": owner_id}
        response = await httpx_client.post(
            url_service=url,
            status_response=201,
            body=owner_vehicle,
            headers=header,
            timeout=40,
        )
        return response

    async def get_all(
        self,
        *,
        query_args: VehicleQueryParams,
    ) -> Optional[List[Vehicle]]:
        url = f"{settings.DATABASE_URL}/api/vehicles"
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

    async def get_vehicle_owners(self, *, vehicle_id: str) -> List[Owner]:
        url = (
            f"{settings.DATABASE_URL}/api/vehicles-x-owners/vehicle/{vehicle_id}/owners"
        )
        header = {"Content-Type": "application/json"}
        response = await httpx_client.get(
            url_service=url, status_response=200, headers=header, timeout=40
        )
        return response

    async def update(
        self, *, vehicle_id: str, vehicle_in: UpdateVehicle
    ) -> VehicleInDB:
        url = f"{settings.DATABASE_URL}/api/vehicles/{vehicle_id}"
        header = {"Content-Type": "application/json"}
        user = vehicle_in.dict()
        response = await httpx_client.patch(
            url_service=url, status_response=200, body=user, headers=header, timeout=40
        )
        return response


vehicle_service = VehicleService()

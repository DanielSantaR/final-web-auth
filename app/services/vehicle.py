from typing import List

from app.core.config import Settings, get_settings
from app.infra.httpx.client import HTTPXClient
from app.schemas.search import VehicleQueryParams
from app.schemas.vehicle import CreateVehicle, UpdateVehicle, Vehicle, VehicleInDB

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

    async def get_all(
        self,
        *,
        query_args: VehicleQueryParams,
    ) -> List[Vehicle]:
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

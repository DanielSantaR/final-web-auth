from app.core.config import Settings, get_settings
from app.infra.httpx.client import HTTPXClient
from app.schemas.vehicle import CreateVehicle, Vehicle

httpx_client = HTTPXClient()

settings: Settings = get_settings()


class VehicleService:
    def __init__(self):
        return

    async def get_vehicle_by_plate(self, *, vehicle_id: int) -> Vehicle:
        url = f"{settings.DATABASE_URL}/api/vehicles/{vehicle_id}"
        header = {"Content-Type": "application/json"}
        response = await httpx_client.get(
            url_service=url, status_response=200, headers=header, timeout=40
        )
        return response

    async def create_vehicle(self, *, vehicle_in: CreateVehicle) -> CreateVehicle:
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


vehicle_service = VehicleService()

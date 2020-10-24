from app import schemas
from app.core.config import Settings, get_settings
from app.infra.httpx.client import HTTPXClient

httpx_client = HTTPXClient()

settings: Settings = get_settings()


async def get_vehicle_by_plate(*, vehicle_id: int) -> schemas.Vehicle:
    url = f"{settings.DATABASE_URL}/api/vehicle/vehicle-id/{vehicle_id}/"
    header = {"Content-Type": "application/json"}
    response = await httpx_client.get(
        url_service=url, status_response=200, headers=header, timeout=40
    )
    return response


async def create_vehicle(*, vehicle_in: schemas.CreateVehicle) -> schemas.CreateVehicle:
    url = f"{settings.DATABASE_URL}/api/vehicle/"
    header = {"Content-Type": "application/json"}
    vehicle = vehicle_in.dict()
    response = await httpx_client.post(
        url_service=url, status_response=201, body=vehicle, headers=header, timeout=40
    )
    return response

from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from app import schemas
from app.api import deps
from app.core.config import Settings, get_settings
from app.schemas.vehicle import CreateVehicle
from app.services.vehicle import create_vehicle, get_vehicle_by_plate

settings: Settings = get_settings()


router = APIRouter()


@router.post("", response_model=schemas.Vehicle)
async def create_vehivle(
    *,
    vehicle_in: schemas.BaseVehicle,
    current_employee: schemas.Employee = Depends(deps.get_current_techician),
) -> Any:
    """
    Create new vehicle.
    """
    vehicle_plate = await get_vehicle_by_plate(vehicle_id=vehicle_in.plate)
    if vehicle_plate:
        raise HTTPException(
            status_code=400,
            detail="The vehicle with this plate already exists in the system.",
        )

    vehicle = CreateVehicle(
        creation_employee=current_employee["identity_card"],
        update_employee=current_employee["identity_card"],
        **vehicle_in.dict(),
    )
    vehicle = await create_vehicle(vehicle_in=vehicle)
    return vehicle

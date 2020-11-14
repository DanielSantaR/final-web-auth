from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from app.api import deps
from app.core.config import Settings, get_settings
from app.schemas.employee import Employee
from app.schemas.vehicle import BaseVehicle, CreateVehicle, Vehicle
from app.services.vehicle import vehicle_service

settings: Settings = get_settings()


router = APIRouter()


@router.post("", response_model=Vehicle)
async def create_vehivle(
    *,
    vehicle_in: BaseVehicle,
    current_employee: Employee = Depends(deps.get_current_techician),
) -> Any:
    """
    Create new vehicle.
    """
    vehicle_plate = await vehicle_service.get_vehicle_by_plate(
        vehicle_id=vehicle_in.plate
    )
    if vehicle_plate:
        raise HTTPException(
            status_code=400,
            detail="The vehicle with this plate already exists in the system.",
        )

    vehicle = CreateVehicle(
        creation_employee_id=current_employee["identity_card"],
        update_employee_id=current_employee["identity_card"],
        **vehicle_in.dict(),
    )
    vehicle = await vehicle_service.create_vehicle(vehicle_in=vehicle)
    return vehicle

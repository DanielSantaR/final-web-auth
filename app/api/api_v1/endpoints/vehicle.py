from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import JSONResponse

from app.api import deps
from app.core.config import Settings, get_settings
from app.schemas.employee import Employee
from app.schemas.owner import Owner
from app.schemas.search import VehicleQueryParams
from app.schemas.vehicle import BaseVehicle, CreateVehicle, UpdateVehicle, Vehicle
from app.services.vehicle import vehicle_service

settings: Settings = get_settings()


router = APIRouter()


@router.post(
    "",
    response_class=JSONResponse,
    response_model=Vehicle,
    status_code=201,
    responses={
        201: {"description": "Vehicles created"},
        401: {"description": "User unauthorized"},
        404: {"description": "Vehicles not found"},
    },
)
async def create_vehicle(
    *,
    vehicle_in: BaseVehicle,
    current_employee: Employee = Depends(deps.get_current_techician),
) -> Any:
    """
    Create new vehicle.
    """
    vehicle_plate = await vehicle_service.get_by_plate(vehicle_id=vehicle_in.plate)
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
    vehicle = await vehicle_service.create(vehicle_in=vehicle)
    return vehicle


@router.get(
    "/{vehicle_id}",
    response_class=JSONResponse,
    response_model=Vehicle,
    status_code=200,
    responses={
        200: {"description": "Vehicle found"},
        401: {"description": "User unauthorized"},
        404: {"description": "Vehicle not found"},
    },
)
async def get_vehicle_by_id(
    *,
    vehicle_id: str,
    current_employee: Employee = Depends(deps.get_current_active_employee),
) -> Any:
    """
    Gets vehicle's information.
    """
    vehicle = await vehicle_service.get_by_plate(vehicle_id=vehicle_id)
    if not vehicle:
        return JSONResponse(status_code=404, content={"detail": "No vehicle found"})
    return vehicle


@router.get(
    "",
    response_class=JSONResponse,
    response_model=List[Vehicle],
    status_code=200,
    responses={
        200: {"description": "Vehicles found"},
        401: {"description": "User unauthorized"},
    },
)
async def get_all(
    *,
    query_args: VehicleQueryParams = Depends(),
    current_employee: Employee = Depends(deps.get_current_active_employee),
):
    vehicles = await vehicle_service.get_all(query_args=query_args)
    if vehicles:
        return vehicles
    return []


@router.get(
    "/{vehicle_id}/vehicles",
    response_class=JSONResponse,
    response_model=List[Owner],
    status_code=200,
    responses={
        200: {"description": "Owner found"},
        401: {"description": "User unauthorized"},
        404: {"description": "Owner not found"},
    },
)
async def get_owners_vehicles(
    *,
    vehicle_id: str,
    current_employee: Employee = Depends(deps.get_current_active_employee),
) -> Any:
    """
    Gets vehicle's owners information.
    """
    owners = await vehicle_service.get_vehicle_owners(vehicle_id=vehicle_id)
    return owners


@router.patch(
    "/{vehicle_id}",
    response_class=JSONResponse,
    response_model=Vehicle,
    status_code=201,
    responses={
        201: {"description": "Vehicle updated"},
        401: {"description": "User unauthorized"},
        404: {"description": "Vehicle not found"},
    },
)
async def update_vehicle(
    *,
    vehicle_id: str,
    vehicle_in: UpdateVehicle,
    current_employee: Employee = Depends(deps.get_current_techician),
) -> Any:
    """
    Update a vehicle's profile.
    """
    vehicle = await vehicle_service.update(vehicle_id=vehicle_id, vehicle_in=vehicle_in)
    if not vehicle:
        return JSONResponse(status_code=404, content={"detail": "No vehicle found"})
    return vehicle


@router.post(
    "/{vehicle_id}",
    response_class=JSONResponse,
    status_code=201,
    responses={
        201: {"description": "Vehicles owner created"},
        401: {"description": "User unauthorized"},
        404: {"description": "Vehicles owner not found"},
    },
)
async def create_owner_vehicle(
    *,
    vehicle_id: str,
    owner_id: str,
    current_employee: Employee = Depends(deps.get_current_techician),
) -> Any:
    """
    Create new owner vehicle.
    """
    vehicle = await vehicle_service.create_owner_vehicle(
        vehicle_id=vehicle_id, owner_id=owner_id
    )
    return vehicle

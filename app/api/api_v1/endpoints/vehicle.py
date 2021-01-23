from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import JSONResponse

from app.api import deps
from app.schemas.employee import Employee
from app.schemas.owner import Owner
from app.schemas.search import VehicleQueryParams
from app.schemas.vehicle import BaseVehicle, CreateVehicle, UpdateVehicle, Vehicle
from app.schemas.vehicle_x_owner import VehicleXOwner
from app.services.owner import owner_service
from app.services.vehicle import vehicle_service
from app.utils.send_email import send_assigned_vehicle, send_updated_vehicle

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
) -> Vehicle:
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
) -> Vehicle:
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
) -> Optional[List[Vehicle]]:
    vehicles = await vehicle_service.get_all(query_args=query_args)
    if vehicles:
        return vehicles
    return []


@router.get(
    "/{vehicle_id}/owners",
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
) -> List[Owner]:
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
) -> Vehicle:
    """
    Update a vehicle's profile.
    """
    vehicle = await vehicle_service.update(
        vehicle_id=vehicle_id,
        vehicle_in=vehicle_in,
        employee_id=current_employee["identity_card"],
    )
    if not vehicle:
        return JSONResponse(status_code=404, content={"detail": "No vehicle found"})

    vehicle_owners = await vehicle_service.get_vehicle_owners(vehicle_id=vehicle_id)
    if vehicle_owners:
        for owner in vehicle_owners:
            await send_updated_vehicle(
                email_to=owner["email"],
            )
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
) -> VehicleXOwner:
    """
    Create new owner vehicle.
    """

    vehicle = await vehicle_service.get_by_plate(vehicle_id=vehicle_id)
    if not vehicle:
        return JSONResponse(status_code=404, content={"detail": "No vehicle found"})

    owner = await owner_service.get_by_id(owner_id=owner_id)
    if not owner:
        return JSONResponse(status_code=404, content={"detail": "No owner found"})

    vehicle_owner = await vehicle_service.create_owner_vehicle(
        vehicle_id=vehicle_id, owner_id=owner_id
    )
    if vehicle_owner:
        await send_assigned_vehicle(
            email_to=owner["email"],
            plate=vehicle["plate"],
            brand=vehicle["brand"],
            model=vehicle["model"],
            color=vehicle["color"],
            vehicle_type=vehicle["vehicle_type"],
        )
    else:
        return JSONResponse(
            status_code=404,
            content={"detail": "The owner is already assigned to the vehicle"},
        )
    return vehicle

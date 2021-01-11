from typing import List, Optional

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from starlette.responses import JSONResponse, Response

from app.api import deps
from app.schemas.employee import Employee
from app.schemas.owner import Owner
from app.schemas.reparation_detail import (
    BaseReparationDetail,
    ReparationDetail,
    UpdateReparationDetail,
)
from app.services.reparation_details import reparation_detail_service
from app.services.owner import owner_service
from app.services.vehicle import vehicle_service
from app.utils.send_email import send_reparation_detail

router = APIRouter()


@router.post(
    "/vehicles/{vehicle_id}/reparation-details",
    response_class=JSONResponse,
    response_model=ReparationDetail,
    status_code=201,
    responses={
        201: {"description": "Reparation detail created"},
        401: {"description": "User unauthorized"},
        404: {"description": "Vehicles not found"},
    },
)
async def create_reparation_detail(
    *,
    vehicle_id: str,
    detail: BaseReparationDetail,
    current_employee: Employee = Depends(deps.get_current_techician),
) -> ReparationDetail:
    """
    Create new reparation detail for the vehicle.
    """
    detail = await reparation_detail_service.create_detail(
        vehicle_id=vehicle_id,
        detail=detail,
        employee_id=current_employee["identity_card"],
    )
    
    if detail:
        vehicle = await vehicle_service.get_by_plate(vehicle_id = vehicle_id)
        owner = await owner_service.get_by_id(owner_id = vehicle["owner_id"])
        await send_reparation_detail(
            email_to=owner["email"],
            description = detail["description"],
            cost = detail["cost"]
        )

    return detail


@router.get(
    "/vehicles/{vehicle_id}/reparation-details",
    response_class=JSONResponse,
    response_model=Optional[List[ReparationDetail]],
    status_code=200,
    responses={
        200: {"description": "Reparation detail found"},
        401: {"description": "User unauthorized"},
        404: {"description": "Reparation detail not found"},
    },
)
async def get_reparation_detail_by_vehicle(
    *,
    vehicle_id: str,
    current_employee: Employee = Depends(deps.get_current_active_employee),
) -> ReparationDetail:
    """
    Gets all vehicle's reparation detail information.
    """
    detail = await reparation_detail_service.get_by_vehicle(vehicle_id=vehicle_id)
    return detail


@router.get(
    "/owner/me/vehicles/{vehicle_id}/reparation-details",
    response_class=JSONResponse,
    response_model=Optional[List[ReparationDetail]],
    status_code=200,
    responses={
        200: {"description": "Reparation detail found"},
        401: {"description": "User unauthorized"},
        404: {"description": "Reparation detail not found"},
    },
)
async def get_reparation_detail_by_owner(
    *,
    vehicle_id: str,
    current_owner: Owner = Depends(deps.get_current_owner),
) -> ReparationDetail:
    """
    Gets all vehicle's reparation detail information by current owner.
    """
    detail = await reparation_detail_service.get_by_owner(
        vehicle_id=vehicle_id, owner_id=current_owner["identity_card"]
    )
    return detail


@router.get(
    "/vehicles/{vehicle_id}/reparation-details/{reparation_id}",
    response_class=JSONResponse,
    response_model=ReparationDetail,
    status_code=200,
    responses={
        200: {"description": "Reparation detail found"},
        401: {"description": "User unauthorized"},
        404: {"description": "Reparation detail not found"},
    },
)
async def get_reparation_detail_by_id(
    *,
    reparation_id: int,
    vehicle_id: str,
    current_employee: Employee = Depends(deps.get_current_active_employee),
) -> ReparationDetail:
    """
    Gets vehicle's reparation detail information.
    """
    detail = await reparation_detail_service.get_by_id(reparation_id=reparation_id)
    if not detail:
        return JSONResponse(
            status_code=404,
            content={
                "detail": f"No reparation detail found for the vehicle {vehicle_id}"
            },
        )
    return detail


@router.patch(
    "/vehicles/{vehicle_id}/reparation-details/{reparation_id}",
    response_class=JSONResponse,
    response_model=ReparationDetail,
    status_code=201,
    responses={
        201: {"description": "Reparation detail created"},
        401: {"description": "User unauthorized"},
        404: {"description": "Vehicles not found"},
    },
)
async def update_reparation_detail(
    *,
    vehicle_id: str,
    reparation_id: int,
    detail: UpdateReparationDetail,
    current_employee: Employee = Depends(deps.get_current_techician),
) -> ReparationDetail:
    """
    Create new reparation detail for the vehicle.
    """
    detail = await reparation_detail_service.update_detail(
        reparation_id=reparation_id,
        detail=detail,
        employee_id=current_employee["identity_card"],
    )
    if not detail:
        return JSONResponse(
            status_code=404,
            content={"detail": f"No reparation detail found for vehicle {vehicle_id}"},
        )
    return detail


@router.delete(
    "/vehicles/{vehicle_id}/reparation-details/{reparation_id}",
    response_class=Response,
    status_code=204,
    responses={
        204: {"description": "VehicleXOwner deleted"},
        401: {"description": "User unauthorized"},
        404: {"description": "VehicleXOwner not found"},
    },
)
async def remove(
    *,
    reparation_id: int,
    vehicle_id: str,
    current_employee: Employee = Depends(deps.get_current_techician),
):
    vehicle_x_owner_remove = await reparation_detail_service.delete_by_id(
        reparation_id=reparation_id
    )
    status_code = 204 if vehicle_x_owner_remove == 1 else 404
    if status_code == 404:
        raise HTTPException(
            status_code=status_code,
            detail=f"No reparation detail found for vehicle {vehicle_id}",
        )
    return Response(status_code=status_code)

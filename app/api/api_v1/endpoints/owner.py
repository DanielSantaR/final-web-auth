from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import JSONResponse, Response

from app.api import deps
from app.core.config import Settings, get_settings
from app.schemas.employee import Employee
from app.schemas.owner import BaseOwner, CreateOwner, Owner, UpdateOwner
from app.schemas.search import OwnerQueryParams
from app.schemas.vehicle import Vehicle
from app.services.owner import owner_service
from app.utils.send_email import send_new_owner

settings: Settings = get_settings()


router = APIRouter()


@router.post(
    "",
    response_class=JSONResponse,
    response_model=Owner,
    status_code=201,
    responses={
        201: {"description": "Owner created"},
        401: {"description": "User unauthorized"},
        404: {"description": "Owner not found"},
    },
)
async def create(
    *,
    owner_in: BaseOwner,
    current_employee: Employee = Depends(deps.get_current_techician),
) -> Any:
    """
    Create new owner.
    """
    owner_id = await owner_service.get_by_id(owner_id=owner_in.identity_card)
    if owner_id:
        raise HTTPException(
            status_code=400,
            detail=f"The owner with id {owner_in.identity_card} already exists in the system.",
        )

    owner = CreateOwner(
        creation_employee_id=current_employee["identity_card"],
        update_employee_id=current_employee["identity_card"],
        **owner_in.dict(),
    )
    owner = await owner_service.create(owner_in=owner)

    if owner_in.email:
        await send_new_owner(
            email_to=owner_in.email,
            identity_card=owner_in.identity_card,
            name=owner_in.names,
            surname=owner_in.surnames,
            phone=owner_in.phone,
        )    
    return owner


@router.get(
    "/me",
    response_class=JSONResponse,
    response_model=Owner,
    status_code=200,
    responses={
        200: {"description": "Owner found"},
        401: {"description": "User unauthorized"},
        404: {"description": "Owner not found"},
    },
)
async def get_profile(
    *,
    current_owner: Owner = Depends(deps.get_current_owner),
) -> Any:
    """
    Gets current owner's profile.
    """
    owner = await owner_service.get_by_id(owner_id=current_owner["identity_card"])
    return owner


@router.get(
    "/vehicles",
    response_class=JSONResponse,
    response_model=List[Vehicle],
    status_code=200,
    responses={
        200: {"description": "Owner found"},
        401: {"description": "User unauthorized"},
        404: {"description": "Owner not found"},
    },
)
async def get_owners_vehicles(
    *,
    current_owner: Owner = Depends(deps.get_current_owner),
) -> Any:
    """
    Gets owner's vehicles information.
    """
    vehicles = await owner_service.get_owner_vehicles(
        owner_id=current_owner["identity_card"]
    )
    return vehicles


@router.get(
    "/{owner_id}",
    response_class=JSONResponse,
    response_model=Owner,
    status_code=200,
    responses={
        200: {"description": "Owner found"},
        401: {"description": "User unauthorized"},
        404: {"description": "Owner not found"},
    },
)
async def get_owner_by_id(
    *,
    owner_id: str,
    current_employee: Employee = Depends(deps.get_current_active_employee),
) -> Any:
    """
    Gets owner's information.
    """
    owner = await owner_service.get_by_id(owner_id=owner_id)
    if not owner:
        return JSONResponse(status_code=404, content={"detail": "No owner found"})
    return owner


@router.get(
    "",
    response_class=JSONResponse,
    response_model=List[Owner],
    status_code=200,
    responses={
        200: {"description": "Owners found"},
        401: {"description": "User unauthorized"},
    },
)
async def get_all(
    *,
    query_args: OwnerQueryParams = Depends(),
    current_employee: Employee = Depends(deps.get_current_active_employee),
):
    owners = await owner_service.get_all(query_args=query_args)
    if owners:
        return owners
    return []


@router.patch(
    "/{owner_id}",
    response_class=JSONResponse,
    response_model=Owner,
    status_code=201,
    responses={
        201: {"description": "Owner updated"},
        401: {"description": "User unauthorized"},
        404: {"description": "Owner not found"},
    },
)
async def update_owner(
    *,
    owner_id: str,
    owner_in: UpdateOwner,
    current_employee: Employee = Depends(deps.get_current_techician),
) -> Any:
    """
    Update a owner's profile.
    """
    owner = await owner_service.update(owner_id=owner_id, owner_in=owner_in)
    if not owner:
        return JSONResponse(status_code=404, content={"detail": "No owner found"})
    return owner


@router.delete(
    "/vehicle/{vehicle_id}/owner_id/{owner_id}",
    response_class=Response,
    status_code=204,
    responses={
        204: {"description": "VehicleXOwner deleted"},
        401: {"description": "User unauthorized"},
        404: {"description": "VehicleXOwner not found"},
    },
)
async def remove(*, owner_id: str, vehicle_id: str):
    vehicle_x_owner_remove = await owner_service.delete(
        owner_id=owner_id, vehicle_id=vehicle_id
    )
    status_code = 204 if vehicle_x_owner_remove == 1 else 404
    return Response(status_code=status_code)

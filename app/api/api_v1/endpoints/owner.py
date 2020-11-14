from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import JSONResponse

from app.api import deps
from app.core.config import Settings, get_settings
from app.schemas.employee import Employee
from app.schemas.owner import BaseOwner, CreateOwner, Owner, UpdateOwner
from app.schemas.search import OwnerQueryParams
from app.services.owner import owner_service

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
    owner_plate = await owner_service.get_by_id(owner_id=owner_in.plate)
    if owner_plate:
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
    return owner


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

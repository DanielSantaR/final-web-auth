from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from app import schemas
from app.api import deps
from app.core.config import Settings, get_settings
from app.services.employee import (
    create_employee,
    get_employee_by_id,
    get_employee_by_username,
)

settings: Settings = get_settings()


router = APIRouter()


@router.post("", response_model=schemas.Employee)
async def create_employee_admin(
    *,
    employee_in: schemas.CreateEmployee,
    current_employee: schemas.Employee = Depends(deps.get_current_assitant),
) -> Any:
    """
    Create new employee.
    """
    employee_username = await get_employee_by_username(username=employee_in.username)
    if employee_username:
        raise HTTPException(
            status_code=400,
            detail="The employee with this username already exists in the system.",
        )

    employee_id = await get_employee_by_id(employee_id=employee_in.identity_card)
    if employee_id:
        raise HTTPException(
            status_code=400,
            detail="The employee with this identity card already exists in the system.",
        )
    employee = await create_employee(employee_in=employee_in)
    # if settings.EMAILS_ENABLED and employee_in.email:
    #     send_new_account_email(
    #         email_to=employee_in.email, username=employee_in.email, password=employee_in.password
    #     )
    return employee


@router.post("/internal", response_model=schemas.Employee)
async def create_employee_internal(*, employee_in: schemas.CreateEmployee,) -> Any:
    """
    Create new employee.
    """
    employee_username = await get_employee_by_username(username=employee_in.username)
    if employee_username:
        raise HTTPException(
            status_code=400,
            detail="The employee with this username already exists in the system.",
        )

    employee_id = await get_employee_by_id(employee_id=employee_in.identity_card)
    if employee_id:
        raise HTTPException(
            status_code=400,
            detail="The employee with this identity card already exists in the system.",
        )
    employee = await create_employee(employee_in=employee_in)
    return employee


@router.get("/me", response_model=schemas.Employee)
async def get_profile(
    *, current_employee: schemas.Employee = Depends(deps.get_current_active_employee),
) -> Any:
    """
    Gets employee's profile.
    """
    employee = await get_employee_by_id(employee_id=current_employee["identity_card"])
    return employee

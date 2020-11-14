from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import JSONResponse

from app.api import deps
from app.core.config import Settings, get_settings
from app.schemas.employee import CreateEmployee, Employee, UpdateEmployee
from app.schemas.search import EmployeeQueryParams
from app.services.employee import employee_service

settings: Settings = get_settings()


router = APIRouter()


@router.post(
    "",
    response_class=JSONResponse,
    response_model=Employee,
    status_code=201,
    responses={
        201: {"description": "Employee created"},
        401: {"description": "User unauthorized"},
        404: {"description": "Employee not found"},
    },
)
async def create_employee_admin(
    *,
    employee_in: CreateEmployee,
    current_employee: Employee = Depends(deps.get_current_assistant),
) -> Any:
    """
    Create new employee.
    """
    employee_username = await employee_service.get_by_username(
        username=employee_in.username
    )
    if employee_username:
        raise HTTPException(
            status_code=400,
            detail="The employee with this username already exists in the system.",
        )

    employee_id = await employee_service.get_by_id(
        employee_id=employee_in.identity_card
    )
    if employee_id:
        raise HTTPException(
            status_code=400,
            detail="The employee with this identity card already exists in the system.",
        )
    employee = await employee_service.create(employee_in=employee_in)
    # if settings.EMAILS_ENABLED and employee_in.email:
    #     send_new_account_email(
    #         email_to=employee_in.email, username=employee_in.email, password=employee_in.password
    #     )
    return employee


@router.post(
    "/internal",
    response_class=JSONResponse,
    response_model=Employee,
    status_code=201,
    responses={
        201: {"description": "Employee created"},
        401: {"description": "User unauthorized"},
        404: {"description": "Employee not found"},
    },
)
async def create_employee_internal(
    *,
    employee_in: CreateEmployee,
) -> Any:
    """
    Create new employee.
    """
    employee_username = await employee_service.get_by_username(
        username=employee_in.username
    )
    if employee_username:
        raise HTTPException(
            status_code=400,
            detail="The employee with this username already exists in the system.",
        )

    employee_id = await employee_service.get_by_id(
        employee_id=employee_in.identity_card
    )
    if employee_id:
        raise HTTPException(
            status_code=400,
            detail="The employee with this identity card already exists in the system.",
        )
    employee = await employee_service.create(employee_in=employee_in)
    return employee


@router.get(
    "/me",
    response_class=JSONResponse,
    response_model=Employee,
    status_code=200,
    responses={
        200: {"description": "Employee found"},
        401: {"description": "User unauthorized"},
        404: {"description": "Employee not found"},
    },
)
async def get_profile(
    *,
    current_employee: Employee = Depends(deps.get_current_active_employee),
) -> Any:
    """
    Gets current employee's profile.
    """
    employee = await employee_service.get_by_id(
        employee_id=current_employee["identity_card"]
    )
    return employee


@router.patch(
    "/{employee_id}",
    response_class=JSONResponse,
    response_model=Employee,
    status_code=201,
    responses={
        201: {"description": "Employee updated"},
        401: {"description": "User unauthorized"},
        404: {"description": "Employee not found"},
    },
)
async def update_employee(
    *,
    employee_id: str,
    employee_in: UpdateEmployee,
    current_employee: Employee = Depends(deps.get_current_assistant),
) -> Any:
    """
    Update a employee's profile.
    """
    employee = await employee_service.update(
        employee_id=employee_id, employee_in=employee_in
    )
    return employee


@router.get(
    "/{employee_id}",
    response_class=JSONResponse,
    response_model=Employee,
    status_code=200,
    responses={
        200: {"description": "Employee found"},
        401: {"description": "User unauthorized"},
        404: {"description": "Employee not found"},
    },
)
async def get_employee_by_id(
    *,
    employee_id: str,
    current_employee: Employee = Depends(deps.get_current_active_employee),
) -> Any:
    """
    Gets employee's profile.
    """
    employee = await employee_service.get_by_id(employee_id=employee_id)
    return employee


@router.get(
    "",
    response_class=JSONResponse,
    response_model=List[Employee],
    status_code=200,
    responses={
        200: {"description": "Employees found"},
        401: {"description": "User unauthorized"},
    },
)
async def get_all(
    *, query_args: EmployeeQueryParams = Depends(), skip: int = 0, limit: int = 99999
):
    employees = await employee_service.get_all(
        query_args=query_args, skip=skip, limit=limit
    )
    if employees:
        return employees
    return []

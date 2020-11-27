from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import JSONResponse

from app.api import deps
from app.core import security
from app.core.config import Settings, get_settings
from app.schemas.owner_token import CreateOwnerToken
from app.schemas.token import Token
from app.services.auth import auth_service
from app.services.owner_token import owner_token_service
from app.utils.send_email import send_code_email

# from app.utils import (
#     generate_password_reset_token,
#     send_reset_password_email,
#     verify_password_reset_token,
# )


settings: Settings = get_settings()
router = APIRouter()


@router.post("/login/access-token", response_model=Token)
async def login_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    employee = await auth_service.authenticate(
        username=form_data.username, password=form_data.password
    )
    if not employee:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not employee.is_active:
        raise HTTPException(status_code=400, detail="Inactive employee")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            employee.identity_card, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/owners/access-token")
async def owner_access_token(identity_card: str) -> Any:
    owner = await auth_service.owner_authenticate(identity_card=identity_card)
    if not owner:
        raise HTTPException(
            status_code=400,
            detail="there is no owner with this document, please contact the workshop staff.",
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    code = security.get_random_alphanumeric_string(8)

    while True:
        response = await owner_token_service.get_by_code(owner_token_id=code)
        if not response:
            break
        code = security.get_random_alphanumeric_string(8)

    owner_token = CreateOwnerToken(
        owner_id=identity_card,
        code=code,
        token=security.create_access_token(
            owner.identity_card, expires_delta=access_token_expires
        ),
        token_type="bearer",
    )
    response = await owner_token_service.create(owner_token_in=owner_token)

    if not response:
        raise HTTPException(
            status_code=400,
            detail="Something went wrong, try again in 5 minutes :(",
        )

    # Enviar correo/mensaje con el código

    flag = send_code_email(
        email_to=owner.email,
        code=code,
    )

    if not flag:
        raise HTTPException(
            status_code=400,
            detail="Something went wrong, try again in 5 minutes :(",
        )

    return True


@router.post(
    "/owners/login",
    response_model=Token,
    response_class=JSONResponse,
    status_code=200,
    responses={
        200: {"description": "Owner logged"},
        401: {"description": "User unauthorized"},
        400: {"description": "Bad request"},
    },
)
async def owner_login(code: str):
    owner_token = await owner_token_service.get_by_code(owner_token_id=code)
    if not owner_token:
        raise HTTPException(
            status_code=400,
            detail="Something went wrong, try logging in again :(",
        )
    await deps.get_current_owner(token=owner_token["token"])
    await owner_token_service.delete(owner_token_id=code)
    return {
        "access_token": owner_token["token"],
        "token_type": owner_token["token_type"],
    }


# @router.post("/login/test-token", response_model=schemas.User)
# def test_token(current_user: models.User = Depends(deps.get_current_user)) -> Any:
#     """
#     Test access token
#     """
#     return current_user


# @router.post("/password-recovery/{email}", response_model=schemas.Msg)
# def recover_password(email: str, db: Session = Depends(deps.get_db)) -> Any:
#     """
#     Password Recovery
#     """
#     user = crud.user.get_by_email(db, email=email)

#     if not user:
#         raise HTTPException(
#             status_code=404,
#             detail="The user with this username does not exist in the system.",
#         )
#     password_reset_token = generate_password_reset_token(email=email)
#     send_reset_password_email(
#         email_to=user.email, email=email, token=password_reset_token
#     )
#     return {"msg": "Password recovery email sent"}


# @router.post("/reset-password/", response_model=schemas.Msg)
# def reset_password(
#     token: str = Body(...),
#     new_password: str = Body(...),
#     db: Session = Depends(deps.get_db),
# ) -> Any:
#     """
#     Reset password
#     """
#     email = verify_password_reset_token(token)
#     if not email:
#         raise HTTPException(status_code=400, detail="Invalid token")
#     user = crud.user.get_by_email(db, email=email)
#     if not user:
#         raise HTTPException(
#             status_code=404,
#             detail="The user with this username does not exist in the system.",
#         )
#     elif not crud.user.is_active(user):
#         raise HTTPException(status_code=400, detail="Inactive user")
#     hashed_password = get_password_hash(new_password)
#     user.hashed_password = hashed_password
#     db.add(user)
#     db.commit()
#     return {"msg": "Password updated successfully"}

from fastapi import HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError

from app import schemas
from app.core.config import Settings, get_settings
from app.services.employee import get_user_by_id

settings: Settings = get_settings()

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/v1/login/access-token")


async def get_current_user(token: str = Security(reusable_oauth2)) -> schemas.User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = await get_user_by_id(token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_active(current_user=Security(get_current_user),):
    if not current_user["is_active"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user",
        )
    return current_user


def get_current_admin(current_user=Security(get_current_user),) -> schemas.User:
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user


def get_current_employee(current_user=Security(get_current_user),) -> schemas.User:
    if current_user["role"] != "employee":
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user

from enum import Enum

from fastapi import APIRouter, status
from pydantic import BaseModel, Field

from app.core.config import Settings, get_settings

router = APIRouter()


class StatusEnum(str, Enum):
    OK = "OK"
    FAILURE = "FAILURE"
    CRITICAL = "CRITICAL"
    UNKNOWN = "UNKNOWN"


class HealthCheck(BaseModel):
    title: str = Field(..., description="Auth microservice")
    description: str = Field(..., description="This is a microservice to authorization")
    version: str = Field(..., description="0.0.1")
    status: StatusEnum = Field(..., description="API current status")
    expire_time: int = Field(..., description="ACCESS TOKEN EXPIRE TIME")


@router.get(
    "/status",
    response_model=HealthCheck,
    status_code=status.HTTP_200_OK,
    tags=["Health Check"],
    summary="Performs health check",
    description="Performs health check and returns information about running service.",
)
def health_check():
    settings: Settings = get_settings()
    return {
        "title": settings.WEB_APP_TITLE,
        "description": settings.WEB_APP_DESCRIPTION,
        "version": settings.WEB_APP_VERSION,
        "status": StatusEnum.OK,
        "expire_time": settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    }

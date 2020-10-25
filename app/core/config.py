import logging
import os
from functools import lru_cache

from pydantic import AnyUrl, BaseSettings

log = logging.getLogger(__name__)


class Settings(BaseSettings):
    testing: bool = os.getenv("TESTING", 0)
    WEB_APP_TITLE: str = os.getenv("WEB_APP_TITLE")
    WEB_APP_DESCRIPTION: str = os.getenv("WEB_APP_DESCRIPTION")
    WEB_APP_VERSION: str = os.getenv("WEB_APP_VERSION")
    API_V1_STR: str = os.getenv("/api/v1")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 8
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    DATABASE_URL: AnyUrl = os.getenv("DATABASE_URL")


@lru_cache()
def get_settings() -> BaseSettings:
    log.info("Loading config settings from the environment...")
    return Settings()

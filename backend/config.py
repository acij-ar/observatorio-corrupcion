from enum import Enum
from typing import Optional, Dict, Any

from pydantic import BaseSettings, AnyHttpUrl, validator


class Environment(Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class Settings(BaseSettings):
    ENVIRONMENT: Environment = Environment.DEVELOPMENT

    # Flask config
    APP_NAME = "ObservatorioCorrupción"
    APP_THREADS_PER_PAGE: int = 5
    APP_CSRF_ENABLED: bool = True
    APP_CSRF_SESSION_KEY: str = "secret"
    APP_SECRET_KEY: str = "secret"
    APP_DEBUG: Optional[bool] = None

    @validator("APP_DEBUG", pre=True)
    def set_app_debug(cls, v: Optional[str], values: Dict[str, Any]):
        return v or values.get("ENVIRONMENT") == Environment.DEVELOPMENT

    ARANGO_HOST: AnyHttpUrl
    ARANGO_DB: str
    ARANGO_USERNAME: str
    ARANGO_PASSWORD: str


settings = Settings()

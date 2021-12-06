from enum import Enum
from typing import Optional, Dict, Any, Union

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

    CACHE_TYPE: str = 'redis'
    CACHE_REDIS_HOST: str = 'redis'
    CACHE_REDIS_PORT: int = 6379
    CACHE_REDIS_DB: Union[str, int] = 0
    CACHE_REDIS_URL: str = 'redis://redis:6379/0'
    CACHE_DEFAULT_TIMEOUT: int = 60*60*4


settings = Settings()


class AppConfig(object):
    APP_NAME = settings.APP_NAME
    FLASK_DEBUG = settings.APP_DEBUG
    THREADS_PER_PAGE = settings.APP_THREADS_PER_PAGE
    CSRF_ENABLED = settings.APP_CSRF_ENABLED
    CSRF_SESSION_KEY = settings.APP_CSRF_SESSION_KEY
    SECRET_KEY = settings.APP_SECRET_KEY

    # Cache config
    CACHE_TYPE = settings.CACHE_TYPE
    CACHE_REDIS_HOST = settings.CACHE_REDIS_HOST
    CACHE_REDIS_PORT = settings.CACHE_REDIS_PORT
    CACHE_REDIS_DB = settings.CACHE_REDIS_DB
    CACHE_REDIS_URL = settings.CACHE_REDIS_URL
    CACHE_DEFAULT_TIMEOUT = settings.CACHE_DEFAULT_TIMEOUT

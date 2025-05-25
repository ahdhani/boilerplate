import logging
from functools import lru_cache

from pydantic import AnyUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    env: str = "DEV"


class DBSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DB_")
    async_url: AnyUrl


@lru_cache()
def get_app_settings():
    return AppSettings()


app_settings = get_app_settings()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ecommerce")

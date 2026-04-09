from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    channel_id: str | None = Field(
        default=None,
        alias="CHANNEL_ID",
    )
    
    log_level: str = Field(default="INFO", alias="APP_LOG_LEVEL")


def get_settings() -> Settings:
    return Settings()

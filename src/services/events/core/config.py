import os
from dotenv import load_dotenv
from pydantic import RedisDsn, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

def is_dev(dev=False):
    if not dev:
        load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file_encoding="utf-8")
    SERVER_HOST: str = Field("localhost")
    SERVER_PORT: int = Field(8001)
    MESSAGES_TRANSFER_DSN: RedisDsn = Field("redis://localhost:6379")
    MESSAGES_TRANSFER_DB_NAME: int = Field(1)
    ONLINE_USERS_STORAGE_DSN: RedisDsn = Field("redis://localhost:6379")
    ONLINE_USERS_STORAGE_DB_NAME: int = Field(2)
    SECURITY_SERVER_DSN: str = Field("http://localhost:8000")


settings = Settings()

import logging
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
    MESSAGE_TRANSFER_DSN: str = "redis://localhost:6379/0"
    ONLINE_USER_STORAGE_DSN: str = "redis://localhost:6379/2"
    TOKEN_STORAGE_DSN: str = "redis://localhost:6379/3"


settings = Settings()


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
logger.addHandler(console_handler)

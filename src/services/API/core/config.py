import logging
import os

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


def is_dev(dev=False):
    if not dev:
        load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='../.env', env_file_encoding='utf-8')
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_USER: str = "postgres"
    POSTGRES_DB: str = "smsplus"
    PG_SOCKET: str = "localhost:5432"
    PG_DSN: str = f"postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{PG_SOCKET}/{POSTGRES_DB}"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 60
    REFRESH_TOKEN_EXPIRE_HOURS: int = 24 * 15
    TOKEN_SECRET_KEY: str = "abracadabra"
    MESSAGE_TRANSFER_DSN: str = "redis://localhost:6379/0"
    USERS_CACHE_DSN: str = "redis://localhost:6379/1"
    ONLINE_USER_STORAGE_DSN: str = "redis://localhost:6379/2"
    TOKEN_STORAGE_DSN: str = "redis://localhost:6379/3"
    CELERY_REDIS_BROKER: str = MESSAGE_TRANSFER_DSN


ONLINE_USERS_STORAGE_DSN = os.getenv("ONLINE_USERS_STORAGE_DSN", "redis://localhost:6379")
ONLINE_USERS_STORAGE_DB_NAME = os.getenv("ONLINE_USERS_STORAGE_DB_NAME", 2)

settings = Settings()

logger = logging.getLogger()
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
logger.addHandler(console_handler)

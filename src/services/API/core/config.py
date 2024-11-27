import logging

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


def is_dev(dev=False):
    if not dev:
        print("ENV")
        load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='../.env', env_file_encoding='utf-8')
    PG_DSN: str = f"postgresql+psycopg://postgres:postgres@localhost:5432/smsplus"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_HOURS: int = 24 * 15
    TOKEN_SECRET_KEY: str = "abracadabra"
    MESSAGE_TRANSFER_DSN: str = "redis://localhost:6379/0"
    USERS_CACHE_DSN: str = "redis://localhost:6379/1"
    ONLINE_USER_STORAGE_DSN: str = "redis://localhost:6379/2"
    TOKEN_STORAGE_DSN: str = "redis://localhost:6379/3"
    CELERY_REDIS_BROKER: str = "redis://localhost:6379/0"


settings = Settings()
print(settings.TOKEN_SECRET_KEY)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
logger.addHandler(console_handler)


print("config!!!!!")
import os
from dotenv import load_dotenv
from pydantic import RedisDsn, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


# SERVER_HOST = os.getenv("SERVER_NAME", "localhost")
# SERVER_PORT = os.getenv("SERVER_PORT", 8001)
#
#
# MESSAGES_TRANSFER_DSN = os.getenv("MESSAGES_TRANSFER_DSN", "redis://localhost:6379")
# MESSAGES_TRANSFER_DB_NAME = os.getenv("MESSAGES_TRANSFER_DB_NAME", 1)
#
# ONLINE_USERS_STORAGE_DSN = os.getenv("ONLINE_USERS_STORAGE_DSN", "redis://localhost:6379")
# ONLINE_USERS_STORAGE_DB_NAME = os.getenv("ONLINE_USERS_STORAGE_DB_NAME", 2)
#
#
# SECURITY_SERVER_DSN = os.getenv("SECURITY_SERVER_DSN", "http://localhost:8000")

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

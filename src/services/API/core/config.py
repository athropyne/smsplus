import logging
import os

from dotenv import load_dotenv

load_dotenv()


def PG_DSN() -> str:
    env = os.getenv("PG_DSN")
    if env is not None:
        POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
        POSTGRES_USER = os.getenv("POSTGRES_USER")
        POSTGRES_DB = os.getenv("POSTGRES_DB")

        return f"postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{env}/{POSTGRES_DB}"
    return "postgresql+psycopg://postgres:postgres@localhost:5432/smsplus"


def ACCESS_TOKEN_EXPIRE_MINUTES() -> int:
    try:
        return int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60 * 30))
    except TypeError:
        raise TypeError("parameter ACCESS_TOKEN_EXPIRE_MINUTES must by integer")


def REFRESH_TOKEN_EXPIRE_HOURS() -> int:
    try:
        return int(os.getenv("REFRESH_TOKEN_EXPIRE_HOURS", 60 * 30))
    except TypeError:
        raise TypeError("parameter REFRESH_TOKEN_EXPIRE_HOURS must by integer")


def TOKEN_SECRET_KEY() -> str:
    return os.getenv("TOKEN_SECRET_KEY", "abracadabra")


def REDIS_DSN() -> str:
    env = os.getenv("REDIS_DSN")
    if env is not None:
        return "redis://redis"
    return "redis://localhost:6379"


def MESSAGE_TRANSFER_REDIS_DBNAME():
    try:
        env = int(os.getenv("MESSAGE_TRANSFER_REDIS_DBNAME", 0))
        return env
    except ValueError:
        raise TypeError("parameter REDIS_DBNAME must by integer")


def USERS_CACHE_REDIS_DBNAME():
    try:
        env = int(os.getenv("USERS_CACHE_REDIS_DBNAME", 1))
        return env
    except ValueError:
        raise TypeError("parameter USERS_CACHE_REDIS_DBNAME must by integer")


def TOKEN_STORAGE_REDIS_DBNAME():
    try:
        env = int(os.getenv("TOKEN_STORAGE_REDIS_DBNAME", 2))
        return env
    except ValueError:
        raise TypeError("parameter TOKEN_STORAGE_REDIS_DBNAME must by integer")


def CELERY_REDIS_BROKER_DSN():
    env = os.getenv("CELERY_REDIS_BROKER_DSN", None)
    if env is not None:
        return f"{env}/{MESSAGE_TRANSFER_REDIS_DBNAME()}"
    return f"redis://localhost:6379/{MESSAGE_TRANSFER_REDIS_DBNAME()}"


# logger = logging.Logger("logger")
# logger.setLevel(logging.INFO)
# handler = logging.Handler()
# formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
# handler.setFormatter(formatter)
# logger.addHandler(handler)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('/app.log')
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(message)s'))
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
logger.addHandler(file_handler)
logger.addHandler(console_handler)

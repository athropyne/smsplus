import os

from dotenv import load_dotenv

load_dotenv()

PG_DSN = os.getenv("PG_DSN", "postgresql+psycopg://postgres:postgres@localhost:5432/smsplus")


def ACCESS_TOKEN_EXPIRE_SECOND() -> int:
    try:
        return int(os.getenv("ACCESS_TOKEN_EXPIRE_SECOND", 60 * 30))
    except TypeError:
        raise Exception("parameter ACCESS_TOKEN_EXPIRE_SECOND must by integer")


def TOKEN_SECRET_KEY() -> str:
    return os.getenv("TOKEN_SECRET_KEY", "abracadabra")


def PG_TRANSACTIONS_AUTOCOMMIT() -> bool:
    exc = Exception("parameter PG_TRANSACTIONS_AUTOCOMMIT must by 0 or 1")
    try:
        value = int(os.getenv("PG_TRANSACTIONS_AUTOCOMMIT", 1))
        if value not in (0, 1): raise exc
        return True if value == 1 else False
    except TypeError:
        raise exc


def ONLINE_USERS_REDIS_CONFIG() -> dict:
    return {
        "host": os.getenv("ONLINE_USERS_HOST", "localhost"),
        "port": int(os.getenv("ONLINE_USERS_PORT", 6379)),
        "db": os.getenv("ONLINE_USERS_DB_NAME", "online"),
        "password": os.getenv("ONLINE_USERS_PASSWORD", None),
        "decode_responses": True,
        # add **kwargs parameters if need
    }

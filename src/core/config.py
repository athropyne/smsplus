import os

from dotenv import load_dotenv

load_dotenv()

PG_DSN = os.getenv("PG_DSN", "postgresql+psycopg://postgres:postgres@localhost:5432/smsplus")


def ACCESS_TOKEN_EXPIRE_SECOND() -> int:
    try:
        return int(os.getenv("ACCESS_TOKEN_EXPIRE_SECOND", 60 * 30))
    except TypeError:
        raise TypeError("parameter ACCESS_TOKEN_EXPIRE_SECOND must by integer")


def TOKEN_SECRET_KEY() -> str:
    return os.getenv("TOKEN_SECRET_KEY", "abracadabra")


def PG_TRANSACTIONS_AUTOCOMMIT() -> bool:
    exc = TypeError("parameter PG_TRANSACTIONS_AUTOCOMMIT must by 0 or 1")
    try:
        value = int(os.getenv("PG_TRANSACTIONS_AUTOCOMMIT", 1))
        if value not in (0, 1): raise exc
        return True if value == 1 else False
    except TypeError:
        raise exc


# def ONLINE_USERS_REDIS_CONFIG() -> dict:
#     return {
#         "host": os.getenv("ONLINE_USERS_HOST", "localhost"),
#         "port": int(os.getenv("ONLINE_USERS_PORT", 6379)),
#         "db": os.getenv("ONLINE_USERS_DB_NAME", "online"),
#         "password": os.getenv("ONLINE_USERS_PASSWORD", None),
#         "decode_responses": True,
#         # add **kwargs parameters if need
#     }


def REDIS_HOST()-> str:
    return os.getenv("REDIS_HOST", "localhost")

def REDIS_PORT()-> int:
    try:
        return int(os.getenv("REDIS_PORT", 6379))
    except TypeError:
        raise  TypeError("parameter REDIS_PORT must by integer")


def REDIS_DBNAME():
    env = os.getenv("REDIS_DBNAME", 0)
    if not isinstance(env, int) and not isinstance(env, str):
        raise TypeError("parameter REDIS_DBNAME must by integer or string")
    return env
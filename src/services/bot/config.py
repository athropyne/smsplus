import os

from dotenv import load_dotenv

load_dotenv()


def API_SERVER_URI():
    return os.getenv("API_SERVER_URI", "http://localhost:8000")


def BOT_TOKEN():
    return os.getenv("BOT_TOKEN")


def MESSAGE_TRANSFER_REDIS_HOST() -> str:
    return os.getenv("MESSAGE_TRANSFER_REDIS_HOST", "localhost")


def MESSAGE_TRANSFER_REDIS_PORT() -> int:
    try:
        return int(os.getenv("MESSAGE_TRANSFER_REDIS_PORT", 6379))
    except TypeError:
        raise TypeError("parameter REDIS_PORT must by integer")


def MESSAGE_TRANSFER_REDIS_DBNAME():
    env = os.getenv("MESSAGE_TRANSFER_REDIS_DBNAME", 0)
    if not isinstance(env, int) and not isinstance(env, str):
        raise TypeError("parameter REDIS_DBNAME must by integer or string")
    return env

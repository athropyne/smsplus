import os

from dotenv import load_dotenv

load_dotenv()


def API_SERVER_URI():
    return os.getenv("API_SERVER_URI", "http://localhost:8000")


def BOT_TOKEN():
    return os.getenv("BOT_TOKEN", "7540272705:AAHD47ouqvtaTTNJBJJvE0shbL4KTzb8vew")


def MESSAGE_TRANSFER_REDIS_HOST() -> str:
    return os.getenv("MESSAGE_TRANSFER_REDIS_HOST", "localhost")


def MESSAGE_TRANSFER_REDIS_PORT() -> int:
    try:
        return int(os.getenv("MESSAGE_TRANSFER_REDIS_PORT", 6379))
    except TypeError:
        raise TypeError("parameter MESSAGE_TRANSFER_REDIS_PORT must by integer")


def REDIS_DSN() -> str:
    return os.getenv("REDIS_DSN")


def MESSAGE_TRANSFER_REDIS_DBNAME():
    try:
        env = int(os.getenv("MESSAGE_TRANSFER_REDIS_DBNAME", 0))
        return env
    except ValueError:
        raise TypeError("parameter REDIS_DBNAME must by integer")

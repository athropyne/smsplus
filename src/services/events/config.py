import os

from dotenv import load_dotenv

load_dotenv()

SERVER_HOST = os.getenv("SERVER_NAME", "localhost")
SERVER_PORT = os.getenv("SERVER_PORT", 8001)


MESSAGES_STORAGE_DSN = os.getenv("MESSAGES_STORAGE_DSN", "redis://localhost:6379")
MESSAGES_STORAGE_DB_NAME = os.getenv("MESSAGES_STORAGE_DB_NAME", 1)


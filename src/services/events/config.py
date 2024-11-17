import os

from dotenv import load_dotenv

load_dotenv()

SERVER_HOST = os.getenv("SERVER_NAME", "localhost")
SERVER_PORT = os.getenv("SERVER_PORT", 8001)

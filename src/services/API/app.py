from contextlib import asynccontextmanager

from starlette.middleware.cors import CORSMiddleware

from core import storages
from modules.messages import messages_router
from modules.security import security_router
from modules.users import users_router
from fastapi import FastAPI

from core.schemas import metadata
from core.storages import Database


@asynccontextmanager
async def lifespan(app: FastAPI):
    database = Database()
    await database.init(metadata)
    await storages.message_transfer.connection.info()
    await storages.users_cache.connection.info()
    await storages.online_user_storage.connection.info()
    await storages.token_storage.connection.info()
    yield
    await database.dispose()
    await storages.message_transfer.connection.aclose(close_connection_pool=True)
    await storages.users_cache.connection.aclose(close_connection_pool=True)
    await storages.online_user_storage.connection.aclose(close_connection_pool=True)
    await storages.token_storage.connection.aclose(close_connection_pool=True)


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(security_router)
app.include_router(users_router)
app.include_router(messages_router)

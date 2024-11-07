from contextlib import asynccontextmanager

from starlette.middleware.cors import CORSMiddleware

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
    yield
    await database.dispose()


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

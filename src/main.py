from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core import storages
from src.core.schemas import metadata
from src.API.modules.security import security_router
from src.API.modules.users import users_router
from src.API.modules.messages import messages_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await storages.Database.init(metadata)
    yield
    await storages.Database.dispose()


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

import datetime

from pydantic import BaseModel, Field


class CreateModel(BaseModel):
    receiver: int
    text: str = Field(max_length=300)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)


class MessageModel(CreateModel):
    sender: int


class TelegramEventModel(CreateModel):
    sender: str


class SystemMessage(BaseModel):
    signal: str

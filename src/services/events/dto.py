from enum import Enum

from pydantic import BaseModel, Field


class EventTypes(str, Enum):
    SIGNAL = "signal"
    MESSAGE = "message"


class Event(BaseModel):
    type: EventTypes
    data: dict | str
# class SystemMessage(BaseModel):
#     data: str

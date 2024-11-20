from pydantic import BaseModel


class SystemMessage(BaseModel):
    signal: str

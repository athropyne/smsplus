from pydantic import BaseModel, Field


class CreateModel(BaseModel):
    to: int
    text: str = Field(max_length=300)

from pydantic import BaseModel, Field


class CreateModel(BaseModel):
    text: str = Field(max_length=300)

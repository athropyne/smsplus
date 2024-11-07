from pydantic import BaseModel, Field


class CreateModel(BaseModel):
    login: str = Field(max_length=30)
    password: str = Field(max_length=100)


class UserInfoModel(BaseModel):
    id: int
    login: str




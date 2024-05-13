from pydantic import BaseModel, Field


class UserLogin(BaseModel):
    username: str = Field(max_length=256, min_length=3)
    password: str = Field(max_length=256, min_length=3)

from pydantic import BaseModel, ConfigDict, Field, AwareDatetime
from typing import Annotated
from datetime import datetime
from apps.users.schemas import UserResponse


class PostBase(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, str_min_length=1)

    title: Annotated[str, Field(max_length=100)]
    content: str


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: Annotated[str | None, Field(max_length=100)] = None
    content: str | None = None


class PostResponse(PostBase):
    id: int
    date_posted: AwareDatetime


class PostResponseDetailed(PostResponse):
    user: UserResponse

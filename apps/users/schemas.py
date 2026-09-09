from pydantic import BaseModel, EmailStr, Field, ConfigDict, AfterValidator, BeforeValidator, field_validator
from typing import Annotated
from fastapi import UploadFile
from core.validators import ImageUploadFile
from core.database import ImageFile


class UserBase(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    email: EmailStr
    username: Annotated[str, Field(min_length=3, max_length=60)]


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    username: Annotated[str | None, Field(min_length=3, max_length=60)] = None
    image: ImageUploadFile | None = None


class UserResponse(UserBase):
    id: int
    image: ImageFile | None = None
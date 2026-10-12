from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field
from pydantic.functional_validators import field_validator

UserStatus = Literal['active', 'blocked', 'deleted']
UserRole = Literal["client", "admin"]

class CreateUser(BaseModel):
    login: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=128)

    @field_validator("login")
    @classmethod
    def validate_login(cls, v: str) -> str:
        v = v.strip()
        if not v.replace("_", "").isalnum():
            raise ValueError("Логин может содержать только буквы, цифры и подчеркивание")
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if v.strip() != v:
            raise ValueError("Пароль не может начинаться с пробела")
        if v.isdigit():
            raise ValueError("Пароль не может состоять только из цифр")
        return v

class LogInUser(BaseModel):
    login: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=1, max_length=128)

class ReadUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    login: str
    status: UserStatus
    role: UserRole
    created_at: datetime


# TODO: дописать валидацию во все методы

from datetime import date, datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

UserStatus = Literal['active', 'blocked', 'deleted']
UserRole = Literal["client", "admin"]

class CreateUser(BaseModel):
    login: str = Field()


# TODO: дописать валидацию во все методы

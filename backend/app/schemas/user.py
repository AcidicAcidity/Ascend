from datetime import date, datetime
from typing import Literal, Any
from pydantic import BaseModel, Field, ConfigDict, model_validator

UserStatus = Literal['active', 'blocked', 'deleted']
UserRole = Literal["client", "admin"]

class CreateUser(BaseModel):
    login: str = Field()


# TODO: дописать валидацию во все методы

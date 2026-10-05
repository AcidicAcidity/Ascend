from datetime import date, datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

Lang = Literal["ru", "en"]
Theme = Literal["black", "white", "retro"]

class CreateCharacter(BaseModel):
    name: str = Field(min_length=3, max_length=40)
    xp_total: int | None = None
    skin: Theme = "black"
    lang: Lang = "ru"

class UpdateCharacter(BaseModel):
    name: str | None = Field(default=None, min_length=3, max_length=40)
    xp_total: int | None = Field(default=None, ge=0)
    strength: int | None = Field(default=None, ge=0, le=100)
    health: int | None = Field(default=None, ge=0, le=100)
    resolve: int | None = Field(default=None, ge=0, le=100)
    craft: int | None = Field(default=None, ge=0, le=100)
    bonds: int | None = Field(default=None, ge=0, le=100)
    resting: bool | None = None
    resting_started_at: datetime | None = None
    # TODO: settings JSONB

class DeleteCharacter(BaseModel):
    pass
    # TODO: на подумать

class ReturnCharacter(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    xp_total: int
    strength: int
    health: int
    resolve: int
    craft: int
    bonds: int
    resting: bool
    resting_started_at: datetime | None
    skin: Theme
    lang: Lang
    intro_seen: bool
    # TODO: settings JSONB
    created_at: datetime


# TODO: дописать валидацию во все методы

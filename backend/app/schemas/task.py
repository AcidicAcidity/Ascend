from datetime import date, datetime
from typing import Literal, Any
from pydantic import BaseModel, Field, ConfigDict, model_validator


StatKey = Literal["strength", "health", "resolve", "craft", "bonds"]
ScheludeType = Literal["once", "daily", "weekly", "interval"]
TaskStatus = Literal["active", "done", "archived", "skipped"]

class CreateTask(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    stat: StatKey
    xp: int = Field(default=0, ge=0, le=500)
    schedule_type: ScheludeType = "once"
    schelude_data: dict[str, Any] | None = None
    next_due: date | None = None
    counts_for_streak: bool = False

class UpdateTask(BaseModel):
    # Обновление полей только если они пришли.
    # Те поля, что пришли пустыми - не обновляются
    title: str | None = Field(default=None, min_length=1, max_length=255)
    stat: StatKey | None = None
    xp: int | None = Field(default=None, ge=0, le=500)
    schedule_type: ScheludeType | None = None
    schelude_data: dict[str, Any] | None = None
    next_due: date | None = None
    counts_for_streak: bool | None = None
    status: TaskStatus | None = None


class DeleteTask(BaseModel):
    #TODO: если понадобиться можно добавить, но по это под вопросом
    pass

class ReturnTask(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    stat: StatKey
    xp: int
    schedule_type: ScheludeType
    schelude_data: dict[str, Any] | None
    next_due: date | None
    counts_for_streak: bool
    status: TaskStatus
    done_at: datetime | None
    created_at: datetime


# TODO: дописать валидацию во все методы

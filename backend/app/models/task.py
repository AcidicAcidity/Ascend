from datetime import datetime, date
from typing import Any
from sqlalchemy import String, Integer, Boolean, Date, CheckConstraint, ForeignKey, BigInteger, Index
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import TIMESTAMP, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.base import Base
from app.models.character import Character
from app.models.user import User
from app.models.quest_link import QuestLink

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    character_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("character.id", ondelete="CASCADE"), nullable=False)

    title: Mapped[str] = mapped_column(String(120), nullable=False)
    stat: Mapped[str] = mapped_column(String(20), nullable=False)
    xp: Mapped[int] = mapped_column(Integer, nullable=False, default=10)

    schelude_type: Mapped[str] = mapped_column(String(20), nullable=False, default="once")
    schelude_data: Mapped[dict[str, Any] | None] = mapped_column(JSONB)
    next_due: Mapped[date | None] = mapped_column(Date)

    counts_for_streak: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    status: Mapped[str] = mapped_column(String(20), nullable=False, default="active")

    done_at: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True))

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default="NOW()"
    )
    character: Mapped["Character"] = relationship(back_populates="tasks")
    quest_links: Mapped[list["QuestLink"]] = relationship(
        back_populates="tasks", cascade="all, delete-orphan"
    )

    __table_args__ = (
        CheckConstraint(
            "stat IN ('strength', 'health', 'resolve', 'craft', 'bonds')",
            name="stat_check",
        ),
        CheckConstraint(
            "(schelude_type = 'once' AND schelude_data IS NULL) OR "
            "(schelude_type = 'daily' AND schelude_data IS NOT NULL) OR "
            "(schelude_type IN ('weekly', 'interval') AND schelude_data IS NOT NULL)",
            name="schelude_check",
        ),
        Index(
            "tasks_today_idx", "character_id", "status", "next_due",
            postgresql_where="status = 'active'",
        ),
        Index(
            "tasks_streak_idx", "character_id", "done_at",
            postgresql_where="counts_for_streak = TRUE AND done_at IS NOT NULL",
        ),
    )

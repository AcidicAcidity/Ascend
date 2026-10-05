from datetime import datetime
from sqlalchemy import BigInteger, String, CheckConstraint, Text, ForeignKey
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from app.base import Base

class GlobalQuest(Base):
    __table_name__ = "global_quests"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, nullable=False)
    character_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("characters.id"), nullable=False)

    title: Mapped[str] = mapped_column(String(120), nullable=False)
    why: Mapped[str] = mapped_column(Text, nullable=False, default="")
    stat: Mapped[str] = mapped_column(String(20), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default='active')

    closed_at: Mapped[datetime] = mapped_column(TIMESTAMP)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, server_default="NOW()")

    __table_args__ = (
        CheckConstraint(
            "stat IN ('strength', 'health', 'resolve', 'craft', 'bonds')",
            name="global_quest_stat_check"
        ),
        CheckConstraint(
            "status IN ('active', 'done', 'archived')",
            name="global_quests_status_check"
        ),
        CheckConstraint(
            "length(trim(title)) > 0", name="global_quests_title_check"
        )
    )

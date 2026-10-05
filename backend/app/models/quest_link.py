from datetime import datetime
from decimal import Decimal
from sqlalchemy import Numeric, CheckConstraint, ForeignKey, BigInteger, UniqueConstraint
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.base import Base
from app.models.task import Task
from app.models.global_quest import GlobalQuest

class QuestLink(Base):
    __tablename__ = "quest_links"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    quest_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("task.id", ondelete="CASCADE"), nullable=False
    )
    weight: Mapped[Decimal] = mapped_column(
        Numeric(4, 2), nullable=False, default=Decimal("1.00")
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default="NOW()"
    )

    quest: Mapped["GlobalQuest"] = relationship(back_populates="tasks_links")
    task: Mapped["Task"] = relationship(back_populates="quest_links")

    __table_args__ = (
        UniqueConstraint("quest_id", "task_id", name="unique"),
        CheckConstraint("weight > 0 AND weight <= 10", name="weight_check"),
    )

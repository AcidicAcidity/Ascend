from datetime import datetime
from sqlalchemy import String, Integer, Boolean, CheckConstraint, ForeignKey, BigInteger
from sqlalchemy.dialects.postgresql import TIMESTAMP, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.base import Base
from app.models.user import User
from app.models.task import Task
from app.models.global_quests import GlobalQuest

class Character(Base):
    __tablename__ = "characters"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"),
        unique=True, nullable=False,
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    xp_total: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    strength: Mapped[int] = mapped_column(Integer, nullable=False, default=0) #Сила
    health: Mapped[int] = mapped_column(Integer, nullable=False, default=0) #Здоровье
    resolve: Mapped[int] = mapped_column(Integer, nullable=False, default=0) #Воля
    craft: Mapped[int] = mapped_column(Integer, nullable=False, default=0) #Мастерство
    bounds: Mapped[int] = mapped_column(Integer, nullable=False, default=0) #Связи

    resting: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    rest_started_at: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True))

    skin: Mapped[str] = mapped_column(String(50), nullable=False, default="black") #Поменять в БД. Это тема
    lang: Mapped[str] = mapped_column(String(5), nullable=False, default="ru")
    intro_screen: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    settings: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)

    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False, server_default="NOW()")

    user: Mapped["User"] = relationship(back_populates="character")
    tasks: Mapped[list["Task"]] = relationship(
        back_populates="character", cascade="all, delete-orphan"
    )
    quests: Mapped[list["GlobalQuest"]] = relationship(
        back_populates="character", cascade="all, delete-orphan"
    )


    __table_args__ = (
        CheckConstraint("xp_total >= 0", name="xp_check"),
        CheckConstraint(
            "strength >= 0 AND health >= 0 AND resolve >= 0 "
            "AND craft >= 0 AND bonds >= 0",
            name="stats_check",
        ),
        CheckConstraint("lenght(trim(name)) > 0", name="name_check")
    )

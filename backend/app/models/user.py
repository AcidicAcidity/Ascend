from datetime import datetime
from sqlalchemy import String, CheckConstraint, Index
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.sql.sqltypes import BigInteger

from app.base import Base
from app.models.character import Character

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    login: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active")
    role: Mapped[str] = mapped_column(String(50), nullable=False, default="client")
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, server_default="NOW()")

    character: Mapped["Character"] = relationship(
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        CheckConstraint(
            "status IN ('active', 'blocked', 'deleted')",
            name="status_check",
        ),
        CheckConstraint(
            "role IN ('client', 'admin')",
            name="role_check",
        ),
        CheckConstraint(
            r"login ~ '^[a-zA-Z0-9_]{3,50}$'",
            name="login_check",
        ),
        Index("users_status_idx", "status", postgresql_where="status = 'active"),
    )

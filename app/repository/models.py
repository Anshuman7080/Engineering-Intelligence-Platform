from app.auth.models import User
from app.conversation.models import Conversation
from uuid import uuid4

from sqlalchemy import (
    String,
    DateTime,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy.sql import func

from app.database.base import Base


class Repository(Base):

    __tablename__ = "repositories"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "repository_name",
            name="uq_user_repository",
        ),
    )

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    user_id: Mapped[str] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    repository_name: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    repository_url: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    user: Mapped["User"] = relationship(
        back_populates="repositories",
        lazy="selectin",
    )

    conversations: Mapped[list["Conversation"]] = relationship(
        back_populates="repository",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
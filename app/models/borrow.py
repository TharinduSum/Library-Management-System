from __future__ import annotations
from datetime import datetime
from enum import StrEnum
from sqlalchemy import String, ForeignKey, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base
from app.models.base import TimestampMixin


class BorrowStatus(StrEnum):
    ACTIVE = "active"
    RETURNED = "returned"
    OVERDUE = "overdue"


class Borrow(Base, TimestampMixin):
    __tablename__ = "borrows"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default=BorrowStatus.ACTIVE)
    borrowed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    due_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    returned_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    notes: Mapped[str | None] = mapped_column(Text)

    user: Mapped["User"] = relationship("User", back_populates="borrows")  # type: ignore
    book: Mapped["Book"] = relationship("Book", back_populates="borrows")  # type: ignore
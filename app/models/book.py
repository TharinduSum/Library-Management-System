from sqlalchemy import String, Integer, Text, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base
from app.models.base import TimestampMixin


class Book(Base, TimestampMixin):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    isbn: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    author: Mapped[str] = mapped_column(String(300), nullable=False)
    publisher: Mapped[str | None] = mapped_column(String(300))
    genre: Mapped[str | None] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(Text)
    total_copies: Mapped[int] = mapped_column(Integer, default=1)
    available_copies: Mapped[int] = mapped_column(Integer, default=1)
    published_year: Mapped[int | None] = mapped_column(Integer)

    borrows: Mapped[list] = relationship("Borrow", back_populates="book")
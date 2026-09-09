from __future__ import annotations
from core.database import intpk, Base, TimeStampMixin, ImageFile
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, date, UTC
from sqlalchemy_file import ImageField
from sqlalchemy import ForeignKey, func
from sqlalchemy.sql.sqltypes import DateTime

class Post(TimeStampMixin, Base):
    __tablename__ = "posts"

    id: Mapped[intpk] = mapped_column(init=False)
    title: Mapped[str]
    content: Mapped[str]
    date_posted: Mapped[datetime] = mapped_column(DateTime(True), default=None, insert_default=lambda: datetime.now(UTC), server_default=func.now())

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), default=None)
    user: Mapped["User"] = relationship(back_populates="posts", default=None, repr=False)
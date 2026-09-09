from __future__ import annotations
from core.database import intpk, Base, TimeStampMixin, ImageFile
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import CITEXT
from datetime import datetime, date, UTC
from sqlalchemy_file import ImageField
from sqlalchemy import ForeignKey, func
from sqlalchemy.sql.sqltypes import DateTime

class User(TimeStampMixin, Base):
    __tablename__ = "users"

    id: Mapped[intpk] = mapped_column(init=False)
    username: Mapped[str] = mapped_column(CITEXT, unique=True)
    email: Mapped[str] = mapped_column(CITEXT, unique=True)
    image: Mapped[ImageFile | None] = mapped_column(default=None)
    posts: Mapped[list["Post"]] = relationship(back_populates="user", default_factory=list, cascade="save-update, merge, delete, delete-orphan", repr=False)
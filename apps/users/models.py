from __future__ import annotations
from core.database import intpk, Base, TimeStampMixin, ImageFile
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import CITEXT
from datetime import datetime, date, UTC
from sqlalchemy_file import ImageField
from dataclasses import InitVar
from sqlalchemy import ForeignKey, func
from sqlalchemy.sql.sqltypes import DateTime
from core.auth import password_hasher


class User(TimeStampMixin, Base):
    __tablename__ = "users"

    id: Mapped[intpk] = mapped_column(init=False)
    username: Mapped[str] = mapped_column(CITEXT, unique=True)
    email: Mapped[str] = mapped_column(CITEXT, unique=True)

    password: InitVar[str]
    repeat_password: InitVar[str]
    password_hash: Mapped[str] = mapped_column(repr=False, init=False)

    image: Mapped[ImageFile | None] = mapped_column(default=None)
    posts: Mapped[list["Post"]] = relationship(
        back_populates="user",
        default_factory=list,
        cascade="save-update, merge, delete, delete-orphan",
        repr=False,
    )

    def __post_init__(self, password: str, repeat_password: str):
        if password != repeat_password:
            raise ValueError("Passwords do not match")
        self.password_hash = password_hasher.hash(password)

    def verify_password(self, password: str) -> bool:
        return password_hasher.verify(password, self.password_hash)

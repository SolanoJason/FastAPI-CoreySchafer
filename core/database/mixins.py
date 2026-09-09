from sqlalchemy.orm import MappedAsDataclass, Mapped, mapped_column
from sqlalchemy.sql.sqltypes import DateTime
from datetime import datetime, UTC
from sqlalchemy import func

class TimeStampMixin(MappedAsDataclass, kw_only=True):
    created_at: Mapped[datetime] = mapped_column(
        DateTime(True),
        insert_default=lambda: datetime.now(UTC),
        server_default=func.now(),
        init=False,
        repr=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(True),
        insert_default=lambda: datetime.now(UTC),
        server_default=func.now(), # check if insert is necessary as onupdate will also set the value on insert
        onupdate=lambda: datetime.now(UTC),
        server_onupdate=func.now(),
        init=False,
        repr=False
    )
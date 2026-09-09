from fastapi import Depends
from .base import SessionFactory
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from collections.abc import AsyncGenerator


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionFactory() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session, scope="function")]

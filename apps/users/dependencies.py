from typing import Annotated
from sqlalchemy import select
from fastapi import Depends, HTTPException, status
from core.auth import oauth2_scheme, verify_access_token
from core.database import SessionDep
from apps.users.models import User

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: SessionDep
):
    user_id = verify_access_token(token)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    session.get(User, user_id)
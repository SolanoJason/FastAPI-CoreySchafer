from fastapi import APIRouter, Request, HTTPException, status
from fastapi.responses import HTMLResponse
from core.database import SessionDep
from apps.users.models import User
from sqlalchemy.orm import selectinload
from core.settings import settings

router = APIRouter(include_in_schema=False)

templates = settings.templates


@router.get("/users/{user_id}", name="get_user")
async def get_user(request: Request, user_id: int, session: SessionDep):
    user = await session.get(User, user_id, options=[selectinload(User.posts)])
    if user:
        return templates.TemplateResponse(request, "user.html", {"user": user})
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

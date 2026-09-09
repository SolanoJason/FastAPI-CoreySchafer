from fastapi import APIRouter, Request, status
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse
from core.settings import settings
from core.database import SessionDep
from apps.blog.models import Post
from sqlalchemy import select
from sqlalchemy.orm import selectinload

templates = settings.templates

router = APIRouter(include_in_schema=False)


@router.get("/", name="index")
@router.get("/posts", name="posts")
async def root(request: Request, session: SessionDep):
    stmt = select(Post).options(selectinload(Post.user))
    posts = (await session.scalars(stmt)).all()
    return templates.TemplateResponse(request, "index.html", {"posts": posts})
from fastapi import APIRouter, status, Query, Path
from typing import Annotated
from fastapi.exceptions import HTTPException
from apps.blog.schemas import PostCreate, PostResponse, PostResponseDetailed, PostUpdate
from datetime import datetime
from apps.blog.models import Post
from zoneinfo import ZoneInfo
from core.database import SessionDep
from sqlalchemy.orm import selectinload
from sqlalchemy import select

router = APIRouter()


@router.get("/posts", response_model=list[PostResponseDetailed])
async def get_posts(session: SessionDep):
    stmt = select(Post).options(selectinload(Post.user))
    posts = (await session.scalars(stmt)).all()
    return posts


@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
async def create_post(post_data: PostCreate, session: SessionDep):
    """
    Create a new post.
    """
    new_post = Post(
        **post_data.model_dump(), date_posted=datetime.now(tz=ZoneInfo("UTC"))
    )
    session.add(new_post)
    await session.commit()
    return new_post


@router.get("/posts/{post_id}", response_model=PostResponseDetailed)
async def get_post(post_id: int, session: SessionDep):
    """
    Get a post by ID.
    """
    post = await session.get(Post, post_id, options=[selectinload(Post.user)])
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found.",
        )
    return post


@router.put("/posts/{post_id}", response_model=PostResponse)
async def update_post(post_id: int, post_data: PostCreate, session: SessionDep):
    """
    Update a post by ID.
    """
    post = await session.get(Post, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found.",
        )
    for key, value in post_data.model_dump().items():
        setattr(post, key, value)
    await session.commit()
    return post


@router.patch("/posts/{post_id}", response_model=PostResponse)
async def partially_update_post(
    post_id: int, post_data: PostUpdate, session: SessionDep
):
    """
    Partially update a post by ID.
    """
    post = await session.get(Post, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found.",
        )
    for key, value in post_data.model_dump(
        exclude_unset=True, exclude_none=True
    ).items():
        setattr(post, key, value)
    await session.commit()
    return post


@router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, session: SessionDep):
    """
    Delete a post by ID.
    """
    post = await session.get(Post, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found.",
        )
    await session.delete(post)
    await session.commit()

from zoneinfo import ZoneInfo
from datetime import datetime
from fastapi import APIRouter, Request, HTTPException, status, UploadFile, File, Form
from core.database import SessionDep
from apps.users.models import User
from apps.users.schemas import UserCreate, UserResponse, UserUpdate
from apps.blog.models import Post
from sqlalchemy import select, exists
from sqlalchemy.orm import selectinload
from typing import Annotated
from pydantic import BaseModel
from apps.blog.schemas import PostCreate, PostResponse

router = APIRouter()


@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(user_data: UserCreate, session: SessionDep):
    """
    Create a new user.
    """
    stmt = select(
        exists(
            select(1).where(
                (User.email == user_data.email) | (User.username == user_data.username)
            )
        )
    )
    existing_user = await session.scalar(stmt)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email or username already exists.",
        )
    new_user = User(**user_data.model_dump())
    session.add(new_user)
    await session.commit()
    return new_user


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, session: SessionDep):
    """
    Get a user by ID.
    """
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )
    return user


@router.get("/users/{user_id}/posts", response_model=list[PostResponse])
async def get_user_posts(user_id: int, session: SessionDep):
    """
    Get posts for a user by user ID.
    """
    user = await session.get(User, user_id, options=[selectinload(User.posts)])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )
    return user.posts


@router.post("/users/{user_id}/posts", response_model=PostResponse)
async def create_user_post(user_id: int, post_data: PostCreate, session: SessionDep):
    """
    Create a new post for a user.
    """
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )
    new_post = Post(
        **post_data.model_dump(),
        user=user,
    )
    session.add(new_post)
    await session.commit()
    return new_post


@router.patch("/users/{user_id}", response_model=UserResponse)
async def partially_update_user(
    user_id: int, user_data: Annotated[UserUpdate, File()], session: SessionDep
):
    """
    Partially update a user's information.
    """
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    # Update only the fields provided in the request
    for field, value in user_data.model_dump(
        exclude_unset=True, exclude_none=True
    ).items():
        setattr(user, field, value)

    await session.commit()
    return user


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, session: SessionDep):
    """
    Delete a user by ID.
    """
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )
    await session.delete(user)
    await session.commit()

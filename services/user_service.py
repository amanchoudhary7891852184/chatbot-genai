import os
import shutil
from fastapi import HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from models.user import Users
from utils.security import hash_password
import schemas.user_schemas as user_schemas
from typing import Optional
from utils.deps import get_current_user



async def get_users(db: AsyncSession):
    try:
        result = await db.execute(select(Users))
        users = result.scalars().all()
        return users
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Could not retrieve users.")

async def get_user_by_id(user_id: int, db: AsyncSession):
    try:
        result = await db.execute(select(Users).filter(Users.id == user_id))
        user = result.scalars().first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id {user_id} not found")
        return user
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Database error occurred.")

async def create_user(user: user_schemas.UserCreate,db: AsyncSession):
    try:

        result = await db.execute(select(Users).filter(Users.email == user.email))
        if result.scalar_one_or_none():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Email already registered")

        hashed_password = hash_password(user.password)
        db_user = Users(**user.model_dump(exclude={"password"}), password=hashed_password)
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Could not create user: {e}"
        )


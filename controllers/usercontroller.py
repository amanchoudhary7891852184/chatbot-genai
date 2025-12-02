from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile
from typing import Optional
import schemas.user_schemas as user_schemas
from services import user_service

async def get_users(db: AsyncSession):
    return await user_service.get_users(db)

async def get_user_by_id(user_id: int, db: AsyncSession):
    return await user_service.get_user_by_id(user_id, db)
